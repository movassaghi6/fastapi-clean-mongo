from typing import Union
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles HTTP exceptions and returns a JSON response.

    Args:
        _: The request instance (not used).
        exc (HTTPException): The HTTP exception raised.

    Returns:
        JSONResponse: A JSON response with the error details and HTTP status code.
    """
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


def http422_error_handler(
    _: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """
    Handles validation errors (both request and Pydantic validation errors) 
    and returns a standardized JSON response.

    Args:
        _: The request instance (not used).
        exc (Union[RequestValidationError, ValidationError]): The validation error.

    Returns:
        JSONResponse: A JSON response with the list of validation errors and status code 422.
    """
    return JSONResponse({"errors": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


# Modify the default validation error response structure in OpenAPI docs
validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}
