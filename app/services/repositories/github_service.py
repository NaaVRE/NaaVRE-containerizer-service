import datetime
import hashlib
import json
import logging
import uuid
from abc import ABC
from time import sleep

import github
import requests
from github import Github
from github import InputGitTreeElement
from retry import retry

from app.models.vl_config import VLConfig
from app.services.container_registries.container_registry import \
    ContainerRegistry
from app.services.repositories.git_repository import GitRepository

logger = logging.getLogger('uvicorn.error')

GITHUB_PREFIX = 'https://github.com/'
GITHUB_API_PREFIX = 'https://api.github.com/'
GITHUB_API_REPOS = GITHUB_API_PREFIX + 'repos'
GITHUB_WORKFLOW_FILENAME = 'build-push-docker.yml'


def get_content_hash(contents):
    contents = contents.encode('utf-8')
    s = hashlib.sha1()
    s.update(('blob %u\0' % len(contents)).encode('utf-8'))
    s.update(contents)
    return s.hexdigest()


class JobNotFoundError(Exception):
    pass


class GithubService(GitRepository, ABC):

    def __init__(self, vl_conf: VLConfig):
        self.github = Github(auth=github.Auth.Token(
                                            token=vl_conf.cell_github_token))

        cell_github_url = vl_conf.cell_github_url
        self.token = vl_conf.cell_github_token
        self.owner = cell_github_url.split(GITHUB_PREFIX)[1].split('/')[0]
        self.repository_name = \
            cell_github_url.split(GITHUB_PREFIX)[1].split('/')[1]
        if '.git' in self.repository_name:
            self.repository_name = self.repository_name.split('.git')[0]
        self.gh_repository = self.github.get_repo(
            self.owner + '/' + self.repository_name)
        self.dispatches_url = (GITHUB_API_REPOS + '/' + self.owner + '/' +
                               self.repository_name + '/actions/workflows/' +
                               GITHUB_WORKFLOW_FILENAME + '/dispatches')
        self.commits_url = (GITHUB_API_REPOS + '/' + self.owner + '/' +
                            self.repository_name + '/commits')
        self.registry = ContainerRegistry(registry_url=vl_conf.registry_url,
                                          token=vl_conf.cell_github_token)
        self.repository_url = cell_github_url

    @retry(github.GithubException, tries=2, delay=0.1, backoff=0.5)
    def commit(self, commit_list=None, force=False):
        content_updated = False
        tree_elements = []
        for commit_item in commit_list:
            commit_path = commit_item["path"] + '/' + commit_item['file_name']
            local_hash = get_content_hash(commit_item["contents"])
            remote_hash = self.gh_repository.get_contents(commit_path).sha
            if local_hash != remote_hash or force:
                content_updated = True
                blob = self.gh_repository.create_git_blob(
                            commit_item["contents"],
                            "utf-8")
                tree_elements.append(InputGitTreeElement(path=commit_path,
                                                         mode="100644",
                                                         type="blob",
                                                         sha=blob.sha))
        if not content_updated:
            image_info = self.registry.query_registry_for_image(
                commit_list[0]['path'])
            if not image_info:
                content_updated = True

        if content_updated or force:
            base_tree = self.gh_repository.get_git_tree(sha="main")
            new_tree = self.gh_repository.create_git_tree(tree=tree_elements,
                                                          base_tree=base_tree)
            # Fetch and merge the latest changes from the remote branch
            self.github.get_repo(
                self.owner + '/' + self.repository_name).get_branch("main")
            parent_commit = self.gh_repository.get_git_commit(
                self.gh_repository.get_branch("main").commit.sha)

            # Create a commit
            commit_message = commit_list[0]['path']
            new_commit = (self.gh_repository.
                          create_git_commit(message=commit_message,
                                            tree=new_tree,
                                            parents=[parent_commit]))

            # Update the reference to point to the new commit
            main_ref = self.gh_repository.get_git_ref("heads/main")
            try:
                main_ref.edit(sha=new_commit.sha)
            except github.GithubException as e:
                if "not a fast-forward" in str(e):
                    raise Exception(
                        "Update failed: not a fast-forward. Ensure the branch "
                        "is up-to-date.")
        return content_updated

    def dispatch_containerization_workflow(self, title=None,
                                           image_version=None):
        wf_id = str(uuid.uuid4())
        wf_creation_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        resp = requests.post(
            url=self.dispatches_url,
            json={
                'ref': 'refs/heads/main',
                'inputs': {
                    'build_dir': title,
                    'dockerfile': 'Dockerfile',
                    'image_repo': self.registry.registry_url,
                    'image_tag': title,
                    'id': wf_id,
                    'image_version': image_version,
                }
            },
            verify=False,
            headers={'Accept': 'application/vnd.github.v3+json',
                     'Authorization': 'token ' + self.token}
        )
        if (resp.status_code != 201 and resp.status_code != 200 and
                resp.status_code != 204):
            raise Exception('Error dispatching workflow: ' + resp.text)
        job = self.get_job(wf_id=wf_id, wf_creation_utc=wf_creation_utc,
                           job_id=None)
        source_url = (self.repository_url.replace('.git', '') + '/tree/' +
                      job['head_sha'] + '/' + title)
        return {'workflow_id': wf_id,
                'workflow_url': job['html_url'],
                'source_url': source_url}

    def get_job(self,
                wf_id=None,
                wf_creation_utc=None,
                job_id=None,
                ):
        f""" Find Github workflow job

        If job_id is set, retrieve it through
        https://api.github.com/repos/{self.owner}/{self.repository_name}
        /actions/jobs/{job_id}

        Else, get all workflows runs created around wf_creation_utc through
        https://api.github.com/repos/{self.owner}/{self.repository_name}
        /actions/runs
        and find the one matching {wf_id}
        """
        if job_id:
            jobs_url = (GITHUB_API_REPOS + '/' + self.owner + '/' +
                        self.repository_name + '/actions/jobs/' + str(job_id))
            self.wait_for_github_api_resources()
            job = self.get_github_workflow_jobs(jobs_url)
            return job
        self.wait_for_github_api_resources()
        job = self.find_job_by_name(job_name=wf_id,
                                    wf_creation_utc=wf_creation_utc)
        return job

    def wait_for_github_api_resources(self):
        rate_limit = self.github.get_rate_limit()
        while rate_limit.core.remaining <= 0:
            reset = rate_limit.core.reset
            # Calculate remaining time for reset
            remaining_time = (reset.timestamp() - datetime.datetime.now().
                              timestamp())
            logger.debug(f'Remaining time for reset: {remaining_time} s')
            logger.debug('API rate exceeded, waiting')
            logger.debug(f'Sleeping for: {remaining_time + 1}')
            sleep(remaining_time + 1)
            rate_limit = self.github.get_rate_limit()

    def get_github_workflow_runs(self, t_utc=None):
        workflow_runs_url = (GITHUB_API_REPOS + '/' + self.owner + '/' +
                             self.repository_name + '/actions/runs')
        if t_utc:
            t_start = (t_utc - datetime.timedelta(minutes=2)).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            t_stop = (t_utc + datetime.timedelta(minutes=2)).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            workflow_runs_url += f"?created={t_start}..{t_stop}"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        workflow_runs = requests.get(url=workflow_runs_url, verify=False,
                                     headers=headers)
        if workflow_runs.status_code != 200:
            return None
        workflow_runs_json = json.loads(workflow_runs.text)
        return workflow_runs_json

    def get_github_workflow_jobs(self, jobs_url=None):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        jobs = requests.get(url=jobs_url, verify=False,
                            headers=headers)
        if jobs.status_code == 200:
            return json.loads(jobs.text)
        else:
            raise Exception(
                'Error getting jobs for workflow run: ' + jobs.text)

    def find_job_by_name(self, job_name=None, wf_creation_utc=None):
        runs = self.get_github_workflow_runs(
            t_utc=wf_creation_utc)
        logger.debug('Got runs: ' + str(len(runs)))
        job = self.get_github_workflow_job(job_name=job_name,
                                           runs=runs['workflow_runs'])
        counter = 0
        while not job:
            logger.debug('No job found, waiting for 2 seconds')
            sleep(3)
            runs = self.get_github_workflow_runs()
            logger.debug('Got runs: ' + str(len(runs)))
            job = self.get_github_workflow_job(job_name=job_name,
                                               runs=runs['workflow_runs'])
            if job:
                return job
            counter += 1
            if counter > 10 and not job:
                break
        raise JobNotFoundError('Job not found: ' + job_name)

    def get_github_workflow_job(self, job_name=None, runs=None):
        for run in runs:
            jobs_url = run['jobs_url']
            self.wait_for_github_api_resources()
            jobs = self.get_github_workflow_jobs(jobs_url)
            for job in jobs['jobs']:
                if job['name'] == job_name:
                    job['head_sha'] = run['head_sha']
                    return job
        return None
