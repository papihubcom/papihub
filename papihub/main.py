import logging.config
import os

from papihub.common.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
import httpx
import uvicorn
from fastapi import FastAPI
from papihub.databases import create_all

from papihub.common.response import json_200, json_500
from papihub.routers import torrents
from papihub.models import *

log = logging.getLogger(__name__)

create_all()

app = FastAPI()

app.include_router(torrents.router)


@app.get("/")
async def root():
    return json_200(message='papihub server')


@app.exception_handler(httpx.HTTPStatusError)
async def http_status_exception_handler(request, e: httpx.HTTPStatusError):
    msg = e.response.json().get('error', {}).get('message')
    log.error('http status exception: ' + msg, exc_info=True)
    return json_500(message=msg)


@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    log.error('universal_exception_handler', exc_info=True)
    return json_500(message=str(exc))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("WEB_PORT", 8000))
