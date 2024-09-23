from typing import Annotated
import logging
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.models.cell import Cell
from app.models.containerizer_payload import ContainerizerPayload
from app.services.base_image_tags import BaseImageTags
from app.services.containerizers.c_containerizer import CContainerizer
from app.services.containerizers.containerizer import Containerizer
from app.services.containerizers.julia_containerizer import JuliaContainerizer
from app.services.containerizers.py_containerizer import PyContainerizer
from app.services.containerizers.r_containerizer import RContainerizer
from app.utils.openid import OpenIDValidator
import uvicorn

app = FastAPI()
security = HTTPBearer()
token_validator = OpenIDValidator()
base_image_tags = BaseImageTags()


if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=10)


def valid_access_token(credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(security)],
        ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail="Not authenticated")




@app.get("/base-image-tags")
def get_base_image_tags(access_token: Annotated[dict, Depends(valid_access_token)]):
    return base_image_tags.get()


def init_containerizer(cell):
    if cell.kernel.lower() == 'python' or cell.kernel == 'ipython':
        return PyContainerizer(cell)
    elif cell.kernel.lower() == 'r' or cell.kernel.lower() == 'irkernel':
        return RContainerizer(cell)
    elif cell.kernel.lower() == 'julia':
        return JuliaContainerizer(cell)
    elif cell.kernel.lower() == 'c':
        return CContainerizer(cell)
    else:
        raise ValueError('Unsupported kernel')



@app.post("/containerize")
def containerize(containerize_payload: ContainerizerPayload):
    conteinerizer = init_containerizer(containerize_payload.cell)
    template_cell = conteinerizer.build_template_cell()
    if conteinerizer.visualization_cell:
        notebook = conteinerizer.extract_notebook()

    environment_template = conteinerizer.build_environment_template()
    docker_template = conteinerizer.build_docker_template()


    conteinerizer.containerize()
    return containerize_payload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)