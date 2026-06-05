from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from TS_TP.domain.task.task_models import TaskModel
from TS_TP.domain.task.task_schemas import FilterTaskSchema


class TaskRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_task: TaskModel) -> TaskModel:
        self._session.add(new_task)
        self._session.flush()
        return new_task

    def get_many(self, filter: FilterTaskSchema) -> dict:
        query = select(TaskModel)

        if filter.title is not None:
            query = query.where(TaskModel.title.contains(filter.title))

        if filter.description is not None:
            query = query.where(
                TaskModel.description.contains(filter.description)
            )

        if filter.start_date is not None:
            query = query.where(TaskModel.start_date == filter.start_date)

        if filter.end_date is not None:
            query = query.where(TaskModel.end_date == filter.end_date)

        if filter.status is not None:
            query = query.where(TaskModel.status == filter.status)

        total = self._session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        users = self._session.scalars(
            query.offset(filter.offset).limit(filter.limit)
        )

        return users.all(), total or 0

    def get_one(self, task_id: UUID) -> TaskModel | None:
        task = self._session.scalar(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        return task
