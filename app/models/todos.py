from sqlmodel import Field

from app.kit.models import RecordModel


class Todos(RecordModel, table=True):
    __tablename__ = "todos"

    description: str = Field(nullable=False)
    completed: bool = Field(default=False, nullable=False)
