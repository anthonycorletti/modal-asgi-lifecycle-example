from typing import AsyncIterator

import pytest_asyncio

from app.kit.postgres import AsyncEngine, create_async_engine
from app.models import RecordModel


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    asyncengine = create_async_engine("app")
    yield asyncengine
    await asyncengine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_test_database(engine: AsyncEngine) -> None:
    async with engine.begin() as cnx:
        await cnx.run_sync(RecordModel.metadata.drop_all)
        await cnx.run_sync(RecordModel.metadata.create_all)
