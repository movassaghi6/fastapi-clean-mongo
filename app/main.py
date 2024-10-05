from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from core.exceptions import http_error_handler
from core.exceptions import http422_error_handler
from api.routes import router as api_router
from core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION
from core.database import create_start_app_handler, create_stop_app_handler



def get_application() -> FastAPI:

    application = FastAPI(title= PROJECT_NAME , debug= DEBUG , version= VERSION)
    
    # Set up event handlers for startup and shutdown
    application.add_event_handler('startup', create_start_app_handler(application))
    application.add_event_handler('shutdown', create_stop_app_handler(application))
    
    # Register custom exception handlers
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    
    # Include the API router
    application.include_router(api_router)
    
    # Set up CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    return application


app = get_application()


