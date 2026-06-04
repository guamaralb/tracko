from uuid import UUID, uuid4

from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.task.task_exc import TaskNotFound
from TS_TP.domain.task.task_models import TaskModel
from TS_TP.domain.task.task_schemas import TaskCreateSchema


def task_service_create(*, uow: UnitOfWork, data: TaskCreateSchema):
    new_task = TaskModel(
        title=data.title,
        creator_user_id=uuid4(),
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
    )

    return uow.tasks.add(new_task)


def task_service_read_one(*, uow: UnitOfWork, task_id: UUID):
    task = uow.tasks.get_one(task_id)

    if not task:
        raise TaskNotFound()
    else:
        return task
