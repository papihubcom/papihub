import logging.config
import os

import inject

from papihub.common.logging import LOGGING_CONFIG
from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.manager.sitemanager import SiteManager

logging.config.dictConfig(LOGGING_CONFIG)
import httpx
import uvicorn
from fastapi import FastAPI
from papihub.databases import create_all

from papihub.common.response import json_200, json_500
from papihub.routers import torrentsroute
from papihub.routers import siteroute
from papihub.models import *
from papihub.tasks import *

log = logging.getLogger(__name__)

create_all()

app = FastAPI()

app.include_router(torrentsroute.router)
app.include_router(siteroute.router)


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


def config(binder):
    loader = SiteParserConfigLoader(conf_path=os.path.join(os.environ.get('WORKDIR'), 'conf', 'parser'))
    binder.bind(SiteParserConfigLoader, loader)
    binder.bind(SiteManager, SiteManager(loader))


if __name__ == "__main__":
    inject.configure(config)
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("WEB_PORT", 8000))
