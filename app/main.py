import os
import json
import time
import traceback

from typing import Union
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.exceptions import http_error_handler
from app.core.exceptions import http422_error_handler
from app.api.routes import router as api_router
from app.core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION, DEPLOYMENT_ENV
from app.core.database import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:

    application = FastAPI(title= PROJECT_NAME , debug= DEBUG , version= VERSION)

    application.add_event_handler('startup', create_start_app_handler(application))
    application.add_event_handler('shutdown', create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    return application


app = get_application()


