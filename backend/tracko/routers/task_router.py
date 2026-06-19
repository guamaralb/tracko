from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from tracko.core.deps import CurrentUserDep, SessionDep
from tracko.core.uow import UnitOfWork
from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskReadManySchema,
    TaskReadOneSchema,
)
from tracko.domain.task.task_services import (
    task_service_create,
    task_service_read_many,
    task_service_read_one,
)

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post(
    '/', response_model=TaskReadOneSchema, status_code=HTTPStatus.CREATED
)
def task_route_create(
    session: SessionDep,
    current_user: CurrentUserDep,
    data: TaskCreateSchema,
) -> TaskModel:
    with UnitOfWork(session) as uow:
        return task_service_create(
            uow=uow, current_user=current_user, data=data
        )


@router.get('/', response_model=TaskReadManySchema, status_code=HTTPStatus.OK)
def user_route_read_many(
    session: SessionDep,
    current_user: CurrentUserDep,
    filter: Annotated[FilterTaskSchema, Query()],
) -> dict:
    with UnitOfWork(session) as uow:
        return task_service_read_many(
            uow=uow, current_user=current_user, filter=filter
        )


@router.get(
    '/{task_id}', response_model=TaskReadOneSchema, status_code=HTTPStatus.OK
)
def task_route_read_one(
    session: SessionDep,
    current_user: CurrentUserDep,
    task_id: UUID,
) -> TaskModel:
    with UnitOfWork(session) as uow:
        return task_service_read_one(
            uow=uow, current_user=current_user, task_id=task_id
        )
