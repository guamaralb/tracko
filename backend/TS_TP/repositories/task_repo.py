from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from TS_TP.domain.task.task_models import TaskModel


class TaskRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_task: TaskModel) -> TaskModel:
        self._session.add(new_task)
        self._session.flush()
        return new_task

    def get_one(self, task_id: UUID) -> TaskModel | None:
        task = self._session.scalar(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        return task
