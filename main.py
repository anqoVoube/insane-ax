import logging

from fastapi import FastAPI
from starlette.requests import Request

from logs.middleware import LoggingMiddleware

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
