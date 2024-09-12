from uuid import uuid4

from httpx import AsyncClient

from app.todos.schemas import TodosCreate, TodosUpdate


async def test_create_todo(client: AsyncClient, todos_create: TodosCreate) -> None:
    response = await client.post("/todos", json=todos_create.model_dump())
    assert response.status_code == 200
    todo = response.json()
    assert todo["description"] == todos_create.description
    assert todo["completed"] == todos_create.completed
    assert todo["id"] is not None
    assert todo["created_at"] is not None
    assert todo["updated_at"] is not None


async def test_list_todos(client: AsyncClient, todos_create: TodosCreate) -> None:
    response = await client.post("/todos", json=todos_create.model_dump())
    assert response.status_code == 200
    todo = response.json()
    response = await client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0] == todo


async def test_show_todo(client: AsyncClient, todos_create: TodosCreate) -> None:
    response = await client.post("/todos", json=todos_create.model_dump())
    assert response.status_code == 200
    todo = response.json()
    response = await client.get(f"/todos/{todo['id']}")
    assert response.status_code == 200
    assert response.json() == todo


async def test_update_todo(
    client: AsyncClient, todos_create: TodosCreate, todos_update: TodosUpdate
) -> None:
    response = await client.post("/todos", json=todos_create.model_dump())
    assert response.status_code == 200
    todo = response.json()
    response = await client.put(f"/todos/{todo['id']}", json=todos_update.model_dump())
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["description"] == todos_update.description
    assert updated_todo["completed"] == todos_update.completed
    assert updated_todo["id"] == todo["id"]
    assert updated_todo["created_at"] == todo["created_at"]
    assert updated_todo["updated_at"] != todo["updated_at"]
    # try to update a non-existing todo
    response = await client.put(f"/todos/{uuid4()}", json=todos_update.model_dump())
    assert response.status_code == 404


async def test_delete_todo(client: AsyncClient, todos_create: TodosCreate) -> None:
    response = await client.post("/todos", json=todos_create.model_dump())
    assert response.status_code == 200
    todo = response.json()
    response = await client.delete(f"/todos/{todo['id']}")
    assert response.status_code == 200
    response = await client.get(f"/todos/{todo['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
    # try to delete a non-existing todo
    response = await client.delete(f"/todos/{uuid4()}")
    assert response.status_code == 404
