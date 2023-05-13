import logging

from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.database import get_session
from logs.middleware import LoggingMiddleware
from models.users import User
from routers.users import user_router

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


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    # TODO: Notification service via gmail or telegram bot
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! You did something wrong. There goes a rainbow..."},
    )


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} You did something wrong. There goes a rainbow..."},
    )


@app.get("/")
async def root(db=Depends(get_session)):
    tom = User(first_name="Tom", last_name="Person")
    db.add(tom)  # добавляем в бд
    await db.commit()
    return {}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


app.include_router(user_router, prefix="/users")
