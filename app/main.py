import json
import logging
import os
from typing import Annotated
from urllib.parse import urlparse

import jwt
import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.containerizer_payload import ContainerizerPayload
from app.models.extractor_payload import ExtractorPayload
from app.models.notebook_data import NotebookData
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
from app.settings import Settings
from app.utils.openid import OpenIDValidator

security = HTTPBearer()
token_validator = OpenIDValidator()


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
    print(current_dir)
    while current_dir != 'NaaVRE-containerizer-service':
        config_path = os.path.join(current_dir, 'configuration.json')
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
    return base_image_tags.get()


def _get_containerizer(cell, virtual_lab: str):
    vl_conf = settings.get_vl_config(virtual_lab)
    if cell.kernel.lower() == 'python' or cell.kernel == 'ipython':
        return PyContainerizer(cell, vl_conf.module_mapping_url)
    elif cell.kernel.lower() == 'r' or cell.kernel.lower() == 'irkernel':
        return RContainerizer(cell, vl_conf.module_mapping_url)
    elif cell.kernel.lower() == 'julia':
        return JuliaContainerizer(cell, vl_conf.module_mapping_url)
    elif cell.kernel.lower() == 'c':
        return CContainerizer(cell, vl_conf.module_mapping_url)
    else:
        raise ValueError('Unsupported kernel')


def _get_github_service(virtual_lab: str):
    vl_conf = settings.get_vl_config(virtual_lab)
    repository_url = vl_conf.cell_github
    if repository_url is None:
        raise ValueError('repository_url not set')
    token = vl_conf.cell_github_token
    if token is None:
        raise ValueError('cell_github_token is not set')
    return GithubService(repository_url=repository_url, token=token)


def _get_extractor(notebook_data: NotebookData):
    extractor = None
    notebook = notebook_data.notebook
    cell_index = notebook_data.cell_index
    kernel = notebook_data.kernel
    if notebook.cells[cell_index].cell_type != 'code':
        # dummy extractor for non-code cells (e.g. markdown)
        extractor = DummyExtractor(notebook_data)
    elif 'r' in kernel.lower():
        extractor = RHeaderExtractor(notebook_data)
    elif 'python' in kernel.lower() or 'ipython' in kernel.lower():
        extractor = PyHeaderExtractor(notebook_data)
    if kernel.lower() == 'irkernel':
        code_extractor = RExtractor(notebook_data)
    elif kernel == 'ipython' or kernel == 'python':
        code_extractor = PyExtractor(notebook_data)
    else:
        raise HTTPException(status_code=400,
                            detail='Unsupported kernel: ' + kernel)
    extractor.mearge_values(code_extractor)
    return extractor


@app.post('/extract_cell')
def extract_cell(access_token: Annotated[dict, Depends(valid_access_token)],
                 extractor_payload: ExtractorPayload):
    extractor_payload.data.set_user_name(access_token['preferred_username'])
    extractor = _get_extractor(extractor_payload.data)
    cell = extractor.get_cell()
    return cell


@app.post('/containerize')
def containerize(access_token: Annotated[dict, Depends(valid_access_token)],
                 containerize_payload: ContainerizerPayload,
                 virtual_lab: str):
    conteinerizer = _get_containerizer(containerize_payload.cell, virtual_lab)
    gh = _get_github_service(virtual_lab)
    cell_contents = conteinerizer.build_script()
    cell_updated = gh.commit(local_content=cell_contents,
                             path=containerize_payload.cell.title,
                             file_name='task' + conteinerizer.file_extension)
    notebook_updated = False
    if conteinerizer.visualization_cell:
        notebook_contents = conteinerizer.extract_notebook()
        notebook_updated = gh.commit(local_content=notebook_contents,
                                     path=containerize_payload.cell.title,
                                     file_name='task.ipynb')

    environment_contents = conteinerizer.build_environment()
    environment_updated = gh.commit(local_content=environment_contents,
                                    path=containerize_payload.cell.title,
                                    file_name='environment.yaml')
    docker_template = conteinerizer.build_docker()
    dockerfile_updated = gh.commit(local_content=docker_template,
                                   path=containerize_payload.cell.title,
                                   file_name='Dockerfile')

    image_version = get_content_hash(cell_contents)[:7]
    container_image = (gh.registry.registry_url + '/' +
                       containerize_payload.cell.title + ':' + image_version)
    containerization_workflow_resp = {'workflow_id': None,
                                      'dispatched_github_workflow': False,
                                      'container_image': container_image,
                                      'workflow_url': None,
                                      'source_url': None}

    if (cell_updated or environment_updated or dockerfile_updated or
            notebook_updated):
        containerization_workflow_resp = gh.dispatch_containerization_workflow(
            title=containerize_payload.cell.title,
            image_version=image_version)
    containerize_payload.cell.container_image = container_image
    return {'workflow_id': containerization_workflow_resp['workflow_id'],
            'dispatched_github_workflow': (
                    cell_updated or environment_updated or dockerfile_updated
                    or notebook_updated),
            'container_image': container_image,
            'workflow_url': containerization_workflow_resp['workflow_url'],
            'source_url': containerization_workflow_resp['source_url']}


@app.get('/containerization-status/{workflow_id}')
def containerization_status(
        access_token: Annotated[dict, Depends(valid_access_token)],
        workflow_id: str,
        virtual_lab: str):
    gh = _get_github_service(virtual_lab)
    job = gh.get_job(wf_id=workflow_id)
    if job is None:
        raise HTTPException(status_code=404,
                            detail='containerization job not found')
    return job


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
