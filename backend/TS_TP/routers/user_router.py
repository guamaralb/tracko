from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from TS_TP.core.deps import SessionDep
from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.user.user_schemas import UserCreateSchema, UserReadSchema
from TS_TP.domain.user.user_services import (
    user_service_create,
    user_service_read_one,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', response_model=UserReadSchema, status_code=HTTPStatus.CREATED
)
def user_route_create(data: UserCreateSchema, session: SessionDep):
    with UnitOfWork(session) as uow:
        return user_service_create(uow=uow, data=data)


@router.get(
    '/{user_id}', response_model=UserReadSchema, status_code=HTTPStatus.OK
)
def user_route_read_one(user_id: UUID, session: SessionDep):
    with UnitOfWork(session) as uow:
        return user_service_read_one(uow=uow, user_id=user_id)
