from typing import Sequence

import structlog
from pydantic import UUID4
from sqlmodel import select

from app.kit.postgres import AsyncSession
from app.models.todos import Todos
from app.todos.schemas import TodosCreate, TodosUpdate

log = structlog.get_logger()


class TodosService:
    async def create(self, session: AsyncSession, todos_create: TodosCreate) -> Todos:
        todo = Todos(**todos_create.model_dump())
        session.add(todo)
        await session.commit()
        return todo

    async def show(self, session: AsyncSession, todo_id: UUID4) -> Todos | None:
        result = await session.exec(select(Todos).where(Todos.id == todo_id))
        return result.one_or_none()

    async def list(self, session: AsyncSession) -> Sequence[Todos]:
        result = await session.exec(select(Todos))
        return result.all()

    async def update(
        self, session: AsyncSession, todo: Todos, todos_update: TodosUpdate
    ) -> Todos:
        for key, value in todos_update.model_dump().items():
            setattr(todo, key, value)
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo

    async def delete(self, session: AsyncSession, todo: Todos) -> None:
        await session.delete(todo)
        await session.commit()
        return None
