from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class TodosBase(BaseModel):
    description: str = Field(..., examples=["ship code to the cloud"])
    completed: Optional[bool] = Field(False, examples=[False])

    class Config:
        json_schema_extra = {
            "example": {
                "description": "ship code to the cloud",
            }
        }


class TodosCreate(TodosBase): ...


class TodosUpdate(TodosBase): ...


class TodosDB(BaseModel):
    id: UUID4
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True
