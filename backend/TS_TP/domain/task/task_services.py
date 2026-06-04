from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.task.task_models import TaskModel
from TS_TP.domain.task.task_schemas import TaskCreateSchema


def task_create_service(*, uow: UnitOfWork, data: TaskCreateSchema):
    new_task = TaskModel(
        title=data.title,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
    )

    return uow.tasks.add(new_task)
