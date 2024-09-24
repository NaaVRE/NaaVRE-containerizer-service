import os
import uuid
from abc import ABC

import hashlib

import requests

from app.services.container_registries.container_registry import ContainerRegistry
from app.services.repositories.gitrepository import GitRepository
from github import Github
from github.GithubException import UnknownObjectException

GITHUB_PREFIX = 'https://github.com/'
GITHUB_API_PREFIX = 'https://api.github.com/'
GITHUB_API_REPOS = GITHUB_API_PREFIX+'repos'
GITHUB_WORKFLOW_FILENAME = 'build-push-docker.yml'


def git_hash(contents):
    s = hashlib.sha1()
    s.update(('blob %u\0' % len(contents)).encode('utf-8'))
    s.update(contents)
    return s.hexdigest()


class GithubService(GitRepository, ABC):

    def __init__(self, repository_url=None, token=None):
        github = Github(token)
        self.token = token
        self.owner = repository_url.split(GITHUB_PREFIX)[1].split('/')[0]
        self.repository_name = repository_url.split(GITHUB_PREFIX)[1].split('/')[1]
        if '.git' in self.repository_name:
            self.repository_name = self.repository_name.split('.git')[0]
        self.gh_repository = github.get_repo(self.owner + '/' + self.repository_name)
        self.dispatches_url = GITHUB_API_REPOS + '/' + self.owner + '/' + self.repository_name + '/actions/workflows/' + GITHUB_WORKFLOW_FILENAME + '/dispatches'
        self.registry = ContainerRegistry()


    def commit(self, local_content=None, path=None, file_name=None):
        try:
            remote_hash = self.gh_repository.get_contents(path=path + '/' + file_name).sha
        except UnknownObjectException:
            remote_hash = None
        local_hash = git_hash(local_content)
        if remote_hash is None:
            self.gh_repository.create_file(
                path=path + '/' + file_name,
                message=path + ' creation',
                content=local_content,
            )
        elif remote_hash != local_hash:
            self.gh_repository.update_file(
                path=path + '/' + file_name,
                message=path + ' update',
                content=local_content,
                sha=remote_hash,
            )
        do_dispatch_containerization_workflow = False
        if os.getenv('DEBUG') and os.getenv('DEBUG').lower() == 'true':
            do_dispatch_containerization_workflow = True
        image_info =  self.registry.query_registry_for_image(path)
        if not image_info:
            do_dispatch_containerization_workflow = True
        if do_dispatch_containerization_workflow:
            self._dispatch_containerization_workflow(task_name=path,dockerfile=None,image=None,image_version=None)

        pass

    def _dispatch_containerization_workflow(self,task_name=None,dockerfile=None,image=None,image_version=None):
        wf_id = str(uuid.uuid4())
        resp = requests.post(
            url=self.dispatches_url,
            json={
                'ref': 'refs/heads/main',
                'inputs': {
                    'build_dir': task_name,
                    'dockerfile': dockerfile,
                    'image_repo': image,
                    'image_tag': task_name,
                    'id': wf_id,
                    'image_version': image_version,
                }
            },
            verify=False,
            headers={'Accept': 'application/vnd.github.v3+json',
                     'Authorization': 'token ' + self.token}
        )
        return resp


