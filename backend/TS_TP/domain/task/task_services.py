from uuid import UUID

from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.task.task_exc import TaskNotFound
from TS_TP.domain.task.task_models import TaskModel
from TS_TP.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskReadManySchema,
)
from TS_TP.domain.user.user_models import UserModel


def task_service_create(
    *, uow: UnitOfWork, current_user: UserModel, data: TaskCreateSchema
) -> TaskModel:
    new_task = TaskModel(
        title=data.title,
        user_id_creator=current_user.id,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
    )

    return uow.tasks.add(new_task)


def task_service_read_many(
    *, uow: UnitOfWork, current_user: UserModel, filter: FilterTaskSchema
) -> TaskReadManySchema:
    tasks, total = uow.tasks.get_many(filter)

    return {
        'tasks': tasks,
        'total': total,
        'offset': filter.offset,
        'limit': filter.limit,
    }


def task_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, task_id: UUID
) -> TaskModel:
    task = uow.tasks.get_one(task_id)

    if not task:
        raise TaskNotFound()
    else:
        return task
