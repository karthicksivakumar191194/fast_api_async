from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from pydantic import ValidationError as RequestValidationError

from app.exceptions import CustomHTTPException


def schema_validation_error_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    Pydantic Schema Validation error exception handler
    """
    formatted_errors = {}

    # Iterate over all the errors from Pydantic
    for error in exc.errors():
        print(error)
        if error["type"] == "missing":
            # If the field is missing from the request
            field_name = error["loc"][-1]
            # TODO: Implement language support for error messages
            formatted_errors[field_name] = "Field required"
        elif error["type"] == "string_too_short":
            field_name = error["loc"][-1]
            # TODO: Implement language support for error messages & format message
            formatted_errors[field_name] = error["msg"]
        elif error["type"] == "value_error":
            field_name = error["loc"][-1]
            # TODO: Implement language support for error messages & format message
            formatted_errors[field_name] = error["msg"]

        # TODO: handle other Pydantic validation errors

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"data": formatted_errors, "message": "Validation error"},
    )


def rate_limit_exceeded_exception_handler(
    request: Request, exc: RateLimitExceeded
):
    """
    Rate limit exceeded exception handler
    """
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"message": "Rate limit exceeded. Please try again later."},
    )


def custom_http_error_exception_handler(
    request: Request, exc: CustomHTTPException
):
    """
    Custom HTTP error exception handler
    """
    content = {"message": exc.detail}

    if exc.STATUS_CODE == status.HTTP_422_UNPROCESSABLE_ENTITY:
        content = {"data": exc.detail, "message": "Validation error"}

    return JSONResponse(
        status_code=exc.STATUS_CODE,
        content=content,
    )
