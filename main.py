import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from logs.middleware import LoggingMiddleware
from routers.users import user_router
from utils.exceptions.validation import ValidationError

app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@app.middleware("http")
async def logs(request: Request, call_next):
    response = await call_next(request)
    LoggingMiddleware(request, response).launch_logging()
    return response


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    # TODO: Notification service via gmail or telegram bot
    return JSONResponse(
        # Change status :) I'm a teapot
        status_code=418,
        content={"message": f"Oops! Something went wrong :("},
    )


@app.exception_handler(ValidationError)
async def unicorn_exception_handler(request: Request, exc: ValidationError):
    # TODO: Notification service via gmail or telegram bot
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


app.include_router(user_router, prefix="/users")
