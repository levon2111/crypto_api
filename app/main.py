import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from app.api import health
from app.api.v1 import crypto
from app.common.error import BadRequest, UnprocessableError
from app.conf.config import Config

app = FastAPI()

app.add_event_handler("startup", Config.app_settings_validate)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=Config.title,
        version=Config.version,
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(BadRequest)
async def bad_request_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_err_resp()


@app.exception_handler(RequestValidationError)
async def invalid_req_handler(
        req: Request,
        exc: RequestValidationError
) -> JSONResponse:
    logging.error(f'Request invalid. {str(exc)}')
    return JSONResponse(
        status_code=400,
        content={
            "type": "about:blank",
            'title': 'Bad Request',
            'status': 400,
            'detail': [str(exc)]
        }
    )


@app.exception_handler(UnprocessableError)
async def unprocessable_error_handler(
        req: Request,
        exc: UnprocessableError
) -> JSONResponse:
    return exc.gen_err_resp()


app.include_router(
    health.router,
    prefix='/health',
    tags=["health"]
)
app.include_router(
    crypto.router,
    prefix='/v1',
    tags=["crypto-currencies v1"]
)
