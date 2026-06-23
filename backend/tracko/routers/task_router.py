from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from tracko.core.deps import CurrentUserDep, SessionDep
from tracko.core.uow import UnitOfWork
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskReadManySchema,
    TaskReadOneSchema,
    TaskUpdateSchema,
)
from tracko.domain.task.task_services import (
    task_service_create,
    task_service_delete,
    task_service_read_many,
    task_service_read_one,
    task_service_update,
)

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', status_code=HTTPStatus.CREATED)
def task_route_create(
    session: SessionDep,
    current_user: CurrentUserDep,
    data: TaskCreateSchema,
) -> TaskReadOneSchema:
    with UnitOfWork(session) as uow:
        return task_service_create(
            uow=uow, current_user=current_user, data=data
        )


@router.get('/', status_code=HTTPStatus.OK)
def task_route_read_many(
    session: SessionDep,
    current_user: CurrentUserDep,
    filter: Annotated[FilterTaskSchema, Query()],
) -> TaskReadManySchema:
    with UnitOfWork(session) as uow:
        return task_service_read_many(
            uow=uow, current_user=current_user, filter=filter
        )


@router.get('/{task_id}', status_code=HTTPStatus.OK)
def task_route_read_one(
    session: SessionDep,
    current_user: CurrentUserDep,
    task_id: UUID,
) -> TaskReadOneSchema:
    with UnitOfWork(session) as uow:
        return task_service_read_one(
            uow=uow, current_user=current_user, task_id=task_id
        )


@router.patch('/{task_id}', status_code=HTTPStatus.OK)
def task_route_update_status(
    session: SessionDep,
    current_user: CurrentUserDep,
    task_id: UUID,
    data: TaskUpdateSchema,
) -> TaskReadOneSchema:
    with UnitOfWork(session) as uow:
        return task_service_update(
            uow=uow, current_user=current_user, task_id=task_id, data=data
        )


@router.delete('/{task_id}', status_code=HTTPStatus.NO_CONTENT)
def task_route_delete(
    session: SessionDep,
    current_user: CurrentUserDep,
    task_id: UUID,
) -> None:
    with UnitOfWork(session) as uow:
        return task_service_delete(
            uow=uow, current_user=current_user, task_id=task_id
        )
