from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

from .store import get_security_json

import enum

class AccessType(enum.Enum):
   FullAccess = 1
   WorkspaceAccess = 2

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


def InitializeSecurity():
    path = "C:\\git\\Research\\fastai\\api_key\\app\\app"
    security_data = get_security_json(path)
    print(security_data)
    global API_KEY_NAME
    global COOKIE_DOMAIN
    try:
        API_KEY_NAME = security_data['API_KEY_NAME']
        COOKIE_DOMAIN = security_data['COOKIE_DOMAIN']
    except:
        print("Critical security information is missing from security.json.")
    print(COOKIE_DOMAIN)



def get_client_api_key(
    api_key_query: str,
    api_key_header: str,
    api_key_cookie: str,
):
    if api_key_query is not None :
        return api_key_query
    elif api_key_header is not None:
        return api_key_header
    elif api_key_cookie is not None:
        return api_key_cookie
    else:
        return None

def check_client_api_key(
    api_key_query: str,
    api_key_header: str,
    api_key_cookie: str,
):
    api_key = get_client_api_key(api_key_query,api_key_header,api_key_cookie)
    if (api_key is None):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="You need to specify an authorization token."
        )
    return api_key

def get_client_access_type(client_api_key):
    accessType = None

    security_data = get_security_json()
    try:
        keys = security_data["API_KEYS"]
        accessTypeStr = keys[client_api_key]
        if (accessTypeStr == "Full"):
            accessType = AccessType.FullAccess
        elif (accessTypeStr == "Workspace"):
            accessType = AccessType.WorkspaceAccess
    except:
        print("api_key not found")
    finally:
        return accessType


async def check_FullAccess(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    client_api_key = check_client_api_key(api_key_query, api_key_header, api_key_cookie)
    access_type = get_client_access_type(client_api_key)
    print(access_type)
    if (access_type == AccessType.FullAccess):
        return client_api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not authorized for this API"
        )

async def check_WorkspaceAccess(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    client_api_key = check_client_api_key(api_key_query, api_key_header, api_key_cookie)
    access_type = get_client_access_type(client_api_key)

    if (access_type == AccessType.FullAccess or access_type == AccessType.WorkspaceAccess):
        return client_api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not authorized for this API"
        )
