import datetime
import json
import logging
import os
from typing import Annotated
from urllib.parse import urlparse

import cachetools.func
import jwt
import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.containerizer_payload import ContainerizerPayload
from app.models.extractor_payload import ExtractorPayload
from app.models.vl_config import VLConfig
from app.services.base_image.base_image_tags import BaseImageTags
from app.services.cell_extractor.extractor import DummyExtractor
from app.services.cell_extractor.py_extractor import PyExtractor
from app.services.cell_extractor.py_header_extractor import PyHeaderExtractor
from app.services.cell_extractor.r_extractor import RExtractor
from app.services.cell_extractor.r_header_extractor import RHeaderExtractor
from app.services.containerizers.c_containerizer import CContainerizer
from app.services.containerizers.julia_containerizer import JuliaContainerizer
from app.services.containerizers.py_containerizer import PyContainerizer
from app.services.containerizers.r_containerizer import RContainerizer
from app.services.repositories.github_service import (GithubService,
                                                      get_content_hash)
from app.settings.service_settings import Settings
from app.utils.openid import OpenIDValidator
from cachetools import TTLCache
from threading import Thread
import time

security = HTTPBearer()
token_validator = OpenIDValidator()


@cachetools.func.ttl_cache(ttl=6 * 3600)
def load_configuration(source):
    # Check if source is a URL
    parsed_url = urlparse(source)
    if parsed_url.scheme in ("http", "https"):  # Remote URL
        response = requests.get(source)
        return response.json()
    elif os.path.exists(source):  # Local file (relative or absolute path)
        with open(source, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
        file.close()
        return data_dict

    else:
        raise Exception('Invalid configuration source')


config_file = os.getenv('CONFIG_FILE_URL', 'https://raw.githubusercontent.com/'
                                           'naavrehub/'
                                           'naavre-workflow-service/'
                                           'main/conf.json')

conf = None
if os.path.exists(config_file):
    conf = load_configuration(config_file)
else:
    # Start going up the directory tree until we find the configuration file
    current_dir = os.getcwd()
    while current_dir != '/':
        config_path = os.path.join(current_dir,
                                   os.getenv('CONFIG_FILE_URL',
                                             'configuration.json'))
        if os.path.exists(config_path):
            conf = load_configuration(config_path)
            break
        current_dir = os.path.dirname(current_dir)

settings = Settings(config=conf)

app = FastAPI(root_path=os.getenv('ROOT_PATH',
                                  '/NaaVRE-containerizer-service'))


if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

containerization_job_cache = TTLCache(maxsize=1000, ttl=86400)


def valid_access_token(credentials: Annotated[
    HTTPAuthorizationCredentials, Depends(security)],
                       ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail='Not authenticated')


@app.get('/base-image-tags')
def get_base_image_tags(
        access_token: Annotated[dict, Depends(valid_access_token)],
        virtual_lab: str):
    vl_conf = settings.get_vl_config(virtual_lab)
    base_image_tags = BaseImageTags(vl_conf.base_image_tags_url)
    return base_image_tags.get_base_image_tags()


def _get_containerizer(containerize_payload: ContainerizerPayload):
    vl_conf = settings.get_vl_config(containerize_payload.virtual_lab)
    if vl_conf is None:
        raise ValueError('virtual lab: ' +
                         containerize_payload.virtual_lab +
                         ' not found in config')
    if (containerize_payload.cell.kernel.lower() == 'python' or
            containerize_payload.cell.kernel == 'ipython'):
        return PyContainerizer(containerize_payload.cell,
                               vl_conf.module_mapping_url)
    elif (containerize_payload.cell.kernel.lower() == 'r' or
          containerize_payload.cell.kernel.lower() == 'irkernel'):
        return RContainerizer(containerize_payload.cell,
                              vl_conf.module_mapping_url)
    elif containerize_payload.cell.kernel.lower() == 'julia':
        return JuliaContainerizer(containerize_payload.cell,
                                  vl_conf.module_mapping_url)
    elif containerize_payload.cell.kernel.lower() == 'c':
        return CContainerizer(containerize_payload.cell,
                              vl_conf.module_mapping_url)
    else:
        raise ValueError('Unsupported kernel')


def _get_github_service(vl_conf: VLConfig):
    repository_url = vl_conf.cell_github_url
    if repository_url is None:
        raise ValueError('repository_url not set')
    token = vl_conf.cell_github_token
    if token is None:
        raise ValueError('cell_github_token is not set')
    logging.debug('Using repository URL: %s', repository_url)
    return GithubService(vl_conf)


def _get_extractor(extractor_payload: ExtractorPayload):
    extractor = None
    notebook = extractor_payload.data.notebook
    cell_index = extractor_payload.data.cell_index
    kernel = extractor_payload.data.kernel
    vl_settings = settings.get_vl_config(extractor_payload.virtual_lab)
    if vl_settings is None:
        raise HTTPException(status_code=400,
                            detail='vl_settings for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if vl_settings.base_image_tags_url is None:
        raise HTTPException(status_code=400,
                            detail='base_image_tags_url for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if vl_settings.module_mapping_url is None:
        raise HTTPException(status_code=400,
                            detail='module_mapping_url for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if vl_settings.cell_github_url is None:
        raise HTTPException(status_code=400,
                            detail='cell_github_url for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if vl_settings.cell_github_token is None:
        raise HTTPException(status_code=400,
                            detail='cell_github_token for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if vl_settings.module_mapping_url is None:
        raise HTTPException(status_code=400,
                            detail='module_mapping_url for: ' +
                            extractor_payload.virtual_lab + ' not found')
    if notebook.cells[cell_index].cell_type != 'code':
        # dummy extractor for non-code cells (e.g. markdown)
        extractor = DummyExtractor(extractor_payload.data,
                                   vl_settings.base_image_tags_url)
    elif 'r' in kernel.lower():
        extractor = RHeaderExtractor(extractor_payload.data,
                                     vl_settings.base_image_tags_url)
    elif 'python' in kernel.lower() or 'ipython' in kernel.lower():
        extractor = PyHeaderExtractor(extractor_payload.data,
                                      vl_settings.base_image_tags_url)
    if not extractor.is_complete():
        if kernel.lower() == 'irkernel':
            code_extractor = RExtractor(extractor_payload.data,
                                        vl_settings.base_image_tags_url)
        elif kernel == 'ipython' or kernel == 'python':
            code_extractor = PyExtractor(extractor_payload.data,
                                         vl_settings.base_image_tags_url)
        else:
            raise HTTPException(status_code=400,
                                detail='Unsupported kernel: ' + kernel)
        extractor.add_missing_values(code_extractor)
    return extractor


def _query_github_job_id(workflow_id, gh_service, wf_creation_utc):
    """
    Function to run in a background thread that polls for the job ID.
    """
    max_retries = 10
    delay = 5  # seconds
    job = gh_service.get_job(wf_id=workflow_id,
                             wf_creation_utc=wf_creation_utc)
    while job is None and max_retries > 0:
        logging.debug('Job not found, retrying in %d seconds...',
                      delay)
        time.sleep(delay)
        job = gh_service.get_job(wf_id=workflow_id,
                                 wf_creation_utc=wf_creation_utc)
        max_retries -= 1
    if job:
        containerization_job_cache[workflow_id] = job['id']


@app.post('/extract_cell')
def extract_cell(access_token: Annotated[dict, Depends(valid_access_token)],
                 extractor_payload: ExtractorPayload):
    extractor_payload.data.set_user_name(access_token['preferred_username'])
    extractor = _get_extractor(extractor_payload)
    if isinstance(extractor, DummyExtractor):
        raise HTTPException(status_code=422,
                            detail='Cell is not a code cell, cannot extract')
    try:
        cell = extractor.get_cell()
    except ValueError as e:
        raise HTTPException(status_code=422,
                            detail='Error extracting cell: ' + str(e))

    if os.getenv('DEBUG', 'false').lower() == 'true':
        test_resource = extractor_payload.model_dump()
        test_resource['cell'] = cell.model_dump()
        with open('/tmp/' + cell.title + '.json', 'w') as f:
            json.dump(test_resource, f, indent=4)
        f.close()
    return cell


@app.post('/containerize')
def containerize(access_token: Annotated[dict, Depends(valid_access_token)],
                 containerize_payload: ContainerizerPayload):
    conteinerizer = _get_containerizer(containerize_payload)
    vl_conf = settings.get_vl_config(containerize_payload.virtual_lab)
    gh = _get_github_service(vl_conf)
    commit_list = []
    cell_contents = conteinerizer.build_script()
    commit_list.append({'contents': cell_contents,
                        'path': containerize_payload.cell.title,
                        'file_name': 'task' + conteinerizer.file_extension})
    environment_contents = conteinerizer.build_environment()
    commit_list.append({'contents': environment_contents,
                        'path': containerize_payload.cell.title,
                        'file_name': 'environment.yaml'})
    docker_template = conteinerizer.build_docker()
    commit_list.append({'contents': docker_template,
                        'path': containerize_payload.cell.title,
                        'file_name': 'Dockerfile'})
    commit_resp = gh.commit(commit_list=commit_list,
                            force=containerize_payload.force_containerize)
    commit_sha = commit_resp['commit_sha']
    source_url = None
    if commit_sha:
        source_url = (gh.repository_url.replace('.git', '') + '/tree/' +
                      commit_sha + '/' + containerize_payload.cell.title)

    image_version = get_content_hash(cell_contents)[:7]
    container_image = (gh.registry.registry_url + '/' +
                       containerize_payload.cell.title + ':' + image_version)
    containerization_workflow_resp = {'workflow_id': None,
                                      'dispatched_github_workflow': False,
                                      'container_image': container_image}

    force_containerize = containerize_payload.force_containerize
    if commit_resp['content_updated'] or force_containerize:
        containerization_workflow_resp = gh.dispatch_containerization_workflow(
            title=containerize_payload.cell.title,
            image_version=image_version)
        wf_creation_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        workflow_id = containerization_workflow_resp.get('workflow_id')
        if workflow_id:
            thread = Thread(
                target=_query_github_job_id,
                args=(workflow_id,
                      gh,
                      wf_creation_utc),
                daemon=True
            )
            thread.start()

        logging.debug('Dispatched containerization workflow for: %s',
                      containerize_payload.cell.title)
    logging.debug('Setting container image: %s', container_image)
    containerize_payload.cell.container_image = container_image
    logging.debug('Containerization workflow response: %s',
                  containerization_workflow_resp)
    return {'workflow_id': containerization_workflow_resp['workflow_id'],
            'dispatched_github_workflow': commit_resp['content_updated'],
            'container_image': container_image,
            'source_url': source_url}


@app.get('/status/{virtual_lab}/{workflow_id}/')
def get_status(
        access_token: Annotated[dict, Depends(valid_access_token)],
        workflow_id: str,
        virtual_lab: str):
    vl_conf = settings.get_vl_config(virtual_lab)
    gh = _get_github_service(vl_conf)
    job_id = containerization_job_cache.get(workflow_id)
    wf_creation_utc = (datetime.datetime.now(tz=datetime.timezone.utc) -
                       datetime.timedelta(hours=24))
    job = gh.get_job(wf_id=workflow_id,
                     job_id=job_id,
                     wf_creation_utc=wf_creation_utc)
    if job is None:
        raise HTTPException(status_code=404,
                            detail='containerization job not found')
    containerization_job_cache[workflow_id] = job['id']

    return {'job': job,
            'workflow_url': workflow_id
            }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='trace')
