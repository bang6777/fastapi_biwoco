from app.container import Container
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

from app.users.adapter.input.api import router as user_router

from core.config import config
from core.db.database import Database
from core.exceptions.custom_exception import CustomException
from core.fastapi.middleware.response_middleware import CustomResponseMiddleware


def init_routers(app_: FastAPI) -> None:
    container = Container()
    user_router.container = container
    app_.include_router(user_router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"success": False, "error_code": exc.error_code,
                     "message": exc.message},
        )

def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(CustomResponseMiddleware),
        Middleware(SentryAsgiMiddleware),
    ]
    return middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database on startup
    Database.connect()
    await Database.setup_indexes()  # Create indexes

    yield  # This pauses the lifespan context, allowing the app to run

    # Close the database connection on shutdown
    await Database.close()
    
sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Biwoco TEST API",
        description="Biwoco TEST API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        middleware=make_middleware(),
        lifespan=lifespan,
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
   
    return app_



app = create_app()
