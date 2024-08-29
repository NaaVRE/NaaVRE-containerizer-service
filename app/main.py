from typing import Annotated
import logging
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from .utils.openid import OpenIDValidator
from .services.base_image_tags import BaseImageTags

app = FastAPI()
security = HTTPBearer()
token_validator = OpenIDValidator()

base_image_tags = BaseImageTags()

if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=10)


def valid_access_token(
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(security)],
        ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/base-image-tags")
def get_base_image_tags(
        access_token: Annotated[dict, Depends(valid_access_token)]
        ):
    return base_image_tags.get()
