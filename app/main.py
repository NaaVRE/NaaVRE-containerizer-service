import logging
import os
from typing import Annotated

import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.containerizer_payload import ContainerizerPayload
from app.services.base_image_tags import BaseImageTags
from app.services.containerizers.c_containerizer import CContainerizer
from app.services.containerizers.julia_containerizer import JuliaContainerizer
from app.services.containerizers.py_containerizer import PyContainerizer
from app.services.containerizers.r_containerizer import RContainerizer
from app.services.repositories.githubservice import GithubService, get_content_hash
from app.utils.openid import OpenIDValidator
from pydantic_settings import BaseSettings




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
app = FastAPI(openapi_url=settings.root_path+"/openapi.json", docs_url=settings.root_path+"/docs")
prefix_router = APIRouter(prefix=settings.root_path)

if os.getenv("DEBUG", "false").lower() == "true":
    logging.basicConfig(level=10)


def valid_access_token(credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(security)],
        ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail="Not authenticated")




@prefix_router.get("/base-image-tags")
def get_base_image_tags(access_token: Annotated[dict, Depends(valid_access_token)]):
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



@prefix_router.post("/containerize")
def containerize(containerize_payload: ContainerizerPayload):
    conteinerizer = _get_containerizer(containerize_payload.cell)
    gh = _get_github_service()
    cell_contents = conteinerizer.build_cell()
    cell_updated = gh.commit(local_content=cell_contents,
                                                      path=containerize_payload.cell.task_name,
                                                      file_name="task"+conteinerizer.file_extension)

    image_version = get_content_hash(cell_contents)[:7]
    notebook_updated = False
    if conteinerizer.visualization_cell:
        notebook_contents = conteinerizer.extract_notebook()
        notebook_updated = gh.commit(local_content=notebook_contents,
                                                          path=containerize_payload.cell.task_name,
                                                          file_name="task.ipynb")
    environment_contents= conteinerizer.build_environment()
    environment_updated = gh.commit(local_content=environment_contents,
                                                      path=containerize_payload.cell.task_name,
                                                      file_name="environment.yaml")
    docker_template = conteinerizer.build_docker()
    dockerfile_updated = gh.commit(local_content=docker_template,
                                                      path=containerize_payload.cell.task_name,
                                                      file_name="Dockerfile")
    containerization_workflow_resp = {"workflow_id": None, "dispatched_github_workflow": False,
                                      "image_version": image_version, "workflow_url": None}

    if cell_updated or environment_updated or dockerfile_updated or notebook_updated:
        containerization_workflow_resp = gh.dispatch_containerization_workflow(task_name=containerize_payload.cell.task_name,
                                              image_version=image_version)
    containerize_payload.cell.image_version = image_version

    return {"workflow_id": containerization_workflow_resp["workflow_id"],
            "dispatched_github_workflow": (cell_updated or environment_updated or dockerfile_updated or notebook_updated),
            "image_version": image_version,
            "workflow_url": containerization_workflow_resp["workflow_url"]}


@app.get("/info")
async def info():
    return {
        "root_path": settings.root_path,
        "openapi_url": settings.root_path+"/openapi.json"
    }

app.include_router(prefix_router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)