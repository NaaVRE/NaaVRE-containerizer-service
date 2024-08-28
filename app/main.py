from typing import Annotated

import jwt

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .utils.openid import OpenIDValidator

app = FastAPI()
security = HTTPBearer()
token_validator = OpenIDValidator()


def valid_access_token(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        ):
    try:
        return token_validator.validate(credentials.credentials)
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.PyJWKClientError):
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/")
def get_root():
    return {"Hello": "World"}


@app.get("/private", )
def get_private(access_token: Annotated[dict, Depends(valid_access_token)]):
    return {"Hello": f"{access_token['preferred_username']}"}
