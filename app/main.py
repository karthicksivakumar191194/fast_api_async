from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.settings import settings
from app.config import language_codes
from app.api.routes import api_router
from app.middleware.localization import DynamicLocalizationMiddleware
from app.exceptions import CustomHTTPException
from app.expection_handlers import (
    rate_limit_exceeded_exception_handler,
    custom_http_error_exception_handler,
    schema_validation_error_exception_handler,
)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    # Initialize the limiter for global rate limiting
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["10/minute"]
    )

    # Create FastAPI App
    fast_api_app = FastAPI()

    # Set the limiter in the state
    fast_api_app.state.limiter = limiter

    # Global exception handling
    fast_api_app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_exception_handler)
    fast_api_app.add_exception_handler(CustomHTTPException, custom_http_error_exception_handler)
    fast_api_app.add_exception_handler(RequestValidationError, schema_validation_error_exception_handler)

    # Include router with versioned prefix
    fast_api_app.include_router(api_router, prefix="")

    # Custom Middlewares
    fast_api_app.add_middleware(DynamicLocalizationMiddleware, default_language="en", supported_languages=language_codes)

    # CORS Middleware
    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add SlowAPIMiddleware and pass the limiter instance to it
    fast_api_app.add_middleware(SlowAPIMiddleware)

    return fast_api_app


# Initialize the app
app = create_app()
