import pytest_asyncio

from app.todos.schemas import TodosBase, TodosCreate, TodosUpdate


@pytest_asyncio.fixture(scope="session")
async def todos_create() -> TodosCreate:
    return TodosCreate.model_validate(TodosBase.Config.json_schema_extra["example"])


@pytest_asyncio.fixture(scope="session")
async def todos_update(
    description: str = "updated and completed todo", completed: bool = True
) -> TodosUpdate:
    return TodosUpdate.model_validate(
        {
            **TodosBase.Config.json_schema_extra["example"],
            **{"description": description, "completed": completed},
        }
    )
