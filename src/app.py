from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.endpoints.order_api import router as orders_router
from src.api.endpoints.health_api import router as health_router
from src.api.errors.api_errors import APIErrorMessage
from src.config.errors import DomainError, ResourceNotFound, RepositoryError
from src.utils import utils

app = FastAPI()
# app.include_router(orders_router, dependencies=[Depends(utils.verify_jwt)])
# app.include_router(health_router, dependencies=[Depends(utils.verify_jwt)])
app.include_router(orders_router)
app.include_router(health_router)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=f"Oops! {exc}")
    return JSONResponse(
        status_code=400,
        content=error_msg.dict(),
    )


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=str(exc))
    return JSONResponse(status_code=404, content=error_msg.dict())


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__, message="Oops! Something went wrong, please try again later..."
    )
    return JSONResponse(
        status_code=500,
        content=error_msg.dict(),
    )


def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema  # type: ignore

    openapi_schema = get_openapi(
        title="Tech Challenge - Módulo 4",
        version="1.0.0",
        description="API para lanchonete do Tech Challenge",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema  # type: ignore


app.openapi = custom_openapi  # type: ignore

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)
