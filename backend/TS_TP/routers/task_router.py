from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from TS_TP.core.deps import SessionDep
from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.task.task_schemas import TaskCreateSchema, TaskReadSchema
from TS_TP.domain.task.task_services import (
    task_service_create,
    task_service_read_one,
)

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post(
    '/', response_model=TaskReadSchema, status_code=HTTPStatus.CREATED
)
def task_route_create(data: TaskCreateSchema, session: SessionDep):
    with UnitOfWork(session) as uow:
        return task_service_create(uow=uow, data=data)


@router.get(
    '/{task_id}', response_model=TaskReadSchema, status_code=HTTPStatus.OK
)
def task_route_read_one(task_id: UUID, session: SessionDep):
    with UnitOfWork(session) as uow:
        return task_service_read_one(uow=uow, task_id=task_id)
