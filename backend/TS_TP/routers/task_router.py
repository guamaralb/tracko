from http import HTTPStatus

from fastapi import APIRouter

from TS_TP.core.deps import SessionDep
from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.task.task_schemas import TaskCreateSchema, TaskReadSchema
from TS_TP.domain.task.task_services import task_create_service

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post(
    '/', response_model=TaskReadSchema, status_code=HTTPStatus.CREATED
)
def task_create_route(data: TaskCreateSchema, session: SessionDep):
    with UnitOfWork(session) as uow:
        return task_create_service(uow=uow, data=data)
