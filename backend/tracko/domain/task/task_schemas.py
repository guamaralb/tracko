from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from tracko.domain.shared.shared_schemas import FilterPageSchema
from tracko.domain.task.task_enums import TaskStatusEnum


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class TaskReadOneSchema(BaseModel):
    id: UUID
    title: str
    user_id_creator: UUID
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: TaskStatusEnum
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskReadManySchema(BaseModel):
    tasks: list[TaskReadOneSchema]
    total: int
    offset: int
    limit: int


class TaskPatchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: TaskStatusEnum


class FilterTaskSchema(FilterPageSchema):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: TaskStatusEnum | None = None
