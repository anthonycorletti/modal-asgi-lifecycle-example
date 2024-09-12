from typing import List, Sequence

import structlog
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import UUID4

from app.kit.postgres import AsyncSession, get_async_db_session
from app.models.todos import Todos
from app.todos.schemas import TodosCreate, TodosDB, TodosUpdate
from app.todos.service import TodosService

router = APIRouter(tags=["todos"])
log = structlog.get_logger()


class Routes:
    create_todo = "/todos"
    list_todos = "/todos"
    show_todo = "/todos/{todo_id}"
    update_todo = "/todos/{todo_id}"
    delete_todo = "/todos/{todo_id}"


@router.post(Routes.create_todo, response_model=TodosDB)
async def _create_todo(
    todos_create: TodosCreate = Body(...),
    todos_svc: TodosService = Depends(TodosService),
    session: AsyncSession = Depends(get_async_db_session),
) -> Todos:
    return await todos_svc.create(session, todos_create)


@router.get(Routes.list_todos, response_model=List[TodosDB])
async def _list_todos(
    todos_svc: TodosService = Depends(TodosService),
    session: AsyncSession = Depends(get_async_db_session),
) -> Sequence[Todos]:
    return await todos_svc.list(session)


@router.get(Routes.show_todo, response_model=TodosDB)
async def _show_todo(
    todo_id: UUID4,
    todos_svc: TodosService = Depends(TodosService),
    session: AsyncSession = Depends(get_async_db_session),
) -> Todos | None:
    todo = await todos_svc.show(session, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.put(Routes.update_todo, response_model=TodosDB)
async def _update_todo(
    todo_id: UUID4,
    todos_update: TodosUpdate = Body(...),
    todos_svc: TodosService = Depends(TodosService),
    session: AsyncSession = Depends(get_async_db_session),
) -> Todos | None:
    todo = await todos_svc.show(session, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return await todos_svc.update(session, todo, todos_update)


@router.delete(Routes.delete_todo, response_model=None)
async def _delete_todo(
    todo_id: UUID4,
    todos_svc: TodosService = Depends(TodosService),
    session: AsyncSession = Depends(get_async_db_session),
) -> None:
    todo = await todos_svc.show(session, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return await todos_svc.delete(session, todo)
