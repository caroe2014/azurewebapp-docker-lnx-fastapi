from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from starlette.responses import RedirectResponse, JSONResponse, PlainTextResponse

#from .routers import items, dynamicWorkspace
from starlette.middleware.cors import CORSMiddleware

from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


#from .security import API_KEY_NAME, COOKIE_DOMAIN, InitializeSecurity, check_FullAccess, check_WorkspaceAccess, get_client_access_type, AccessType
#from .store import get_static_path
# NOTE: Config the path to the permanent storage in config.py

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
# app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,  allow_methods=["*"],  allow_headers=["*"])

STATIC_PATH = "/mnt/"
# STATIC_PATH = "C:/users/v-edcaro/repros/python"
print(STATIC_PATH)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/static/json-tools/index.html')
    return response

@app.get("/static")
async def redirect():
    response = RedirectResponse(url='/static/index.html')
    return response

@app.get("/staticapp")
async def redirect():
    response = RedirectResponse(url='/static/app/index.html')
    return response

@app.get("/static2")
async def redirect():
    response = RedirectResponse(url='/static2/index.html')
    return response

@app.get("/static2app")
async def redirect():
    response = RedirectResponse(url='/static2/app/index.html')
    return response

@app.get("/users/")
async def get_users():
   user =[{'user': 'Adam', 'job': 'Global Security'}, {'user': 'Ramya', 'job': 'Support Engineer'}, {'user': 'Edisom', 'job': 'Technical Advisor'}]
   return user

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)