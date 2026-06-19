from uuid import UUID

from tracko.core.uow import UnitOfWork
from tracko.domain.task.task_exc import TaskNotFound
from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskReadManySchema,
    TaskReadOneSchema,
)
from tracko.domain.user.user_models import UserModel


def task_service_create(
    *, uow: UnitOfWork, current_user: UserModel, data: TaskCreateSchema
) -> TaskReadOneSchema:
    new_task = TaskModel(
        title=data.title,
        user_id_creator=current_user.id,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    task_db = uow.tasks.add(new_task)
    return TaskReadOneSchema.model_validate(task_db)


def task_service_read_many(
    *, uow: UnitOfWork, current_user: UserModel, filter: FilterTaskSchema
) -> TaskReadManySchema:
    tasks_db, total = uow.tasks.get_many(filter)

    return TaskReadManySchema(
        tasks=[TaskReadOneSchema.model_validate(t) for t in tasks_db],
        total=total,
        offset=filter.offset,
        limit=filter.limit,
    )


def task_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, task_id: UUID
) -> TaskReadOneSchema:
    task_db = uow.tasks.get_one(task_id)
    if not task_db:
        raise TaskNotFound()
    return TaskReadOneSchema.model_validate(task_db)
