from uuid import UUID

from fastapi import HTTPException, status

from tracko.core.uow import UnitOfWork
from tracko.domain.task.task_exc import TaskNotFound
from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskReadManySchema,
    TaskReadOneSchema,
    TaskUpdateSchema,
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
    tasks_db, total = uow.tasks.get_many(
        user_id=current_user.id, filter=filter
    )

    return TaskReadManySchema(
        tasks=[TaskReadOneSchema.model_validate(t) for t in tasks_db],
        total=total,
        offset=filter.offset,
        limit=filter.limit,
    )


def task_service_update(
    uow: UnitOfWork,
    current_user: UserModel,
    task_id: UUID,
    data: TaskUpdateSchema,
) -> TaskReadOneSchema:

    # Chama o método que criamos no repositório
    updated_task = uow.tasks.update(
        user_id=current_user.id, task_id=task_id, status=data.status
    )

    # Se retornou None, a tarefa não existe ou é de outro usuário
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tarefa não encontrada ou não pertence a você.',
        )

    return TaskReadOneSchema.model_validate(updated_task)


def task_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, task_id: UUID
) -> TaskReadOneSchema:
    # Adicionamos o user_id aqui
    task_db = uow.tasks.get_one(user_id=current_user.id, task_id=task_id)
    if not task_db:
        raise TaskNotFound()
    return TaskReadOneSchema.model_validate(task_db)


def task_service_delete(
    *, uow: UnitOfWork, current_user: UserModel, task_id: UUID
) -> None:
    # E adicionamos o user_id aqui também
    task_db = uow.tasks.get_one(user_id=current_user.id, task_id=task_id)
    if not task_db:
        raise TaskNotFound()

    uow.tasks.delete(task_db)
