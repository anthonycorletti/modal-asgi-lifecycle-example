import os
from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import structlog
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app import __version__
from app.kit.postgres import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    create_async_sessionmaker,
)
from app.logging import configure_logging
from app.router import router

log = structlog.get_logger()

os.environ["TZ"] = "UTC"


def generate_unique_openapi_id(route: APIRoute) -> str:
    return f"{route.tags[0]}:{route.name}"


class State(TypedDict):
    asyncengine: AsyncEngine
    asyncsessionmaker: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    asyncengine = create_async_engine("app")
    asyncsessionmaker = create_async_sessionmaker(asyncengine)
    log.info("app started")
    yield {"asyncengine": asyncengine, "asyncsessionmaker": asyncsessionmaker}
    await asyncengine.dispose()
    log.info("app stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title="modal-asgi-lifecycle-example",
        generate_unique_id_function=generate_unique_openapi_id,
        version=__version__,
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


configure_logging()
app = create_app()
