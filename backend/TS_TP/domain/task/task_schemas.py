from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from TS_TP.domain.task.task_enums import TaskStatusEnum


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class TaskReadSchema(BaseModel):
    id: UUID
    title: str
    creator_user_id: UUID
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: TaskStatusEnum
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListReadSchema(BaseModel):
    tasks: list[TaskReadSchema]
    total: int


class TaskPatchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: TaskStatusEnum
