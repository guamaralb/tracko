from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import FilterTaskSchema


class TaskRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, new_task: TaskModel) -> TaskModel:
        self._session.add(new_task)
        self._session.flush()
        return new_task

    def get_many(
        self, user_id: UUID, filter: FilterTaskSchema
    ) -> tuple[Sequence[TaskModel], int]:

        # 2. TRAVA DE SEGURANÇA: A query já nasce filtrando pelo dono!
        query = select(TaskModel).where(TaskModel.user_id_creator == user_id)

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

        tasks = self._session.scalars(
            query.offset(filter.offset).limit(filter.limit)
        )

        return tasks.all(), total or 0

    def get_one(self, user_id: UUID, task_id: UUID) -> TaskModel | None:
        task = self._session.scalar(
            select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id_creator == user_id
            )
        )
        return task

    def update(
        self, user_id: UUID, task_id: UUID, status: str
    ) -> TaskModel | None:

        # 1. Busca a tarefa aplicando os dois filtros de uma vez só
        task = self._session.scalar(
            select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id_creator == user_id
            )
        )

        # 2. Se não achou (ou se for de outro usuário), barra aqui
        if not task:
            return None

        # 3. Atualiza e salva
        task.status = status
        self._session.flush()

        return task

    def delete(self, db_task: TaskModel) -> None:
        self._session.delete(db_task)
        self._session.flush()
