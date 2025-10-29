from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette_exporter import handle_metrics, PrometheusMiddleware

from src.prospect_acquisition_agent.api import lifespan
from src.prospect_acquisition_agent.api.middleware import TraceIdMiddleware
from src.prospect_acquisition_agent.api.routes import health
from src.prospect_acquisition_agent.config.logging import get_logger
from src.prospect_acquisition_agent.models.response import (
    ApiResponseModel,
    ApiResponseItemModel,
)

logger = get_logger(__name__)


app = FastAPI(
    title="ENP AI POC",
    summary="Engineering Platform AI POC",
    lifespan=lifespan,
)

app.add_middleware(TraceIdMiddleware)
app.add_middleware(PrometheusMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Global exception handler for request validation errors
    (includes validation errors from request body, query parameters, and path parameters)

    :param request: The incoming HTTP request
    :param exc: The validation exception containing error details
    :return: JSONResponse with status 422 and formatted validation errors
    """
    details = list(
        map(
            lambda error: ApiResponseItemModel(
                field=".".join(map(str, error["loc"])),
                value=str(error.get("input", "")),
                info=error["msg"],
            ),
            exc.errors(),
        )
    )

    response = ApiResponseModel(message="Validation error", details=details)
    return JSONResponse(status_code=422, content=response.model_dump())


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for all unhandled errors

    :param request: The incoming HTTP request
    :param exc: The exception that was raised
    :return: JSONResponse with status 500 and formatted error message
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    details = [
        ApiResponseItemModel(
            field="error",
            value="",
            info="Internal server error",
        )
    ]

    response = ApiResponseModel(message="Internal server error", details=details)

    return JSONResponse(status_code=500, content=response.model_dump())


# routes
app.add_route("/metrics", handle_metrics)
app.include_router(health.router, tags=["health"])
