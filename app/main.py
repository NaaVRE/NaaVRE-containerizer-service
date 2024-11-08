import logging
import os
from typing import Annotated

import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_settings import BaseSettings

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
from app.utils.openid import OpenIDValidator

security = HTTPBearer()
token_validator = OpenIDValidator()
base_image_tags = BaseImageTags()


class Settings(BaseSettings):
    root_path: str = "my-root-path"
    if not root_path.startswith("/"):
        root_path = "/" + root_path
    if root_path.endswith("/"):
        root_path = root_path[:-1]


settings = Settings()

app = FastAPI(root_path=settings.root_path)

if os.getenv("DEBUG", "false").lower() == "true":
    logging.basicConfig(level=10)


def valid_access_token(credentials: Annotated[
    HTTPAuthorizationCredentials, Depends(security)],
                       ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/base-image-tags")
def get_base_image_tags(
        access_token: Annotated[dict, Depends(valid_access_token)]):
    return base_image_tags.get()


def _get_containerizer(cell):
    if cell.kernel.lower() == "python" or cell.kernel == "ipython":
        return PyContainerizer(cell)
    elif cell.kernel.lower() == "r" or cell.kernel.lower() == "irkernel":
        return RContainerizer(cell)
    elif cell.kernel.lower() == "julia":
        return JuliaContainerizer(cell)
    elif cell.kernel.lower() == "c":
        return CContainerizer(cell)
    else:
        raise ValueError("Unsupported kernel")


def _get_github_service():
    repository_url = os.getenv("CELL_GITHUB")
    if repository_url is None:
        raise ValueError("CELL_GITHUB environment variable is not set")
    token = os.getenv("CELL_GITHUB_TOKEN")
    if token is None:
        raise ValueError("CELL_GITHUB environment variable is not set")
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
                            detail="Unsupported kernel: " + kernel)
    extractor.mearge_values(code_extractor)
    return extractor


@app.post("/extract_cell")
def extract_cell(access_token: Annotated[dict, Depends(valid_access_token)],
                 extractor_payload: ExtractorPayload):
    extractor_payload.data.set_user_name(access_token['preferred_username'])
    extractor = _get_extractor(extractor_payload.data)
    cell = extractor.get_cell()
    return cell


@app.post("/containerize")
def containerize(access_token: Annotated[dict, Depends(valid_access_token)],
                 containerize_payload: ContainerizerPayload):
    conteinerizer = _get_containerizer(containerize_payload.cell)
    gh = _get_github_service()
    cell_contents = conteinerizer.build_script()
    cell_updated = gh.commit(local_content=cell_contents,
                             path=containerize_payload.cell.task_name,
                             file_name="task" + conteinerizer.file_extension)

    image_version = get_content_hash(cell_contents)[:7]
    notebook_updated = False
    if conteinerizer.visualization_cell:
        notebook_contents = conteinerizer.extract_notebook()
        notebook_updated = gh.commit(local_content=notebook_contents,
                                     path=containerize_payload.cell.task_name,
                                     file_name="task.ipynb")
    environment_contents = conteinerizer.build_environment()
    environment_updated = gh.commit(local_content=environment_contents,
                                    path=containerize_payload.cell.task_name,
                                    file_name="environment.yaml")
    docker_template = conteinerizer.build_docker()
    dockerfile_updated = gh.commit(local_content=docker_template,
                                   path=containerize_payload.cell.task_name,
                                   file_name="Dockerfile")
    containerization_workflow_resp = {"workflow_id": None,
                                      "dispatched_github_workflow": False,
                                      "image_version": image_version,
                                      "workflow_url": None}

    if (cell_updated or environment_updated or dockerfile_updated or
            notebook_updated):
        containerization_workflow_resp = gh.dispatch_containerization_workflow(
            task_name=containerize_payload.cell.task_name,
            image_version=image_version)
    containerize_payload.cell.image_version = image_version

    return {"workflow_id": containerization_workflow_resp["workflow_id"],
            "dispatched_github_workflow": (
                    cell_updated or environment_updated or dockerfile_updated
                    or notebook_updated), "image_version": image_version,
            "workflow_url": containerization_workflow_resp["workflow_url"]}


@app.get("/containerization-status/{workflow_id}")
def containerization_status(
        access_token: Annotated[dict, Depends(valid_access_token)],
        workflow_id: str):
    gh = _get_github_service()
    job = gh.get_job(wf_id=workflow_id)
    if job is None:
        raise HTTPException(status_code=404,
                            detail="containerization job not found")
    return job


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
