from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from TS_TP.core.deps import CurrentUserDep, SessionDep
from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.user.user_models import UserModel
from TS_TP.domain.user.user_schemas import (
    FilterUserSchema,
    UserCreateSchema,
    UserReadManySchema,
    UserReadOneSchema,
)
from TS_TP.domain.user.user_services import (
    user_service_create,
    user_service_read_many,
    user_service_read_one,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', response_model=UserReadOneSchema, status_code=HTTPStatus.CREATED
)
def user_route_create(
    session: SessionDep,
    current_user: CurrentUserDep,
    data: UserCreateSchema,
) -> UserModel:
    with UnitOfWork(session) as uow:
        return user_service_create(
            uow=uow, current_user=current_user, data=data
        )


@router.get('/', response_model=UserReadManySchema, status_code=HTTPStatus.OK)
def user_route_read_many(
    session: SessionDep,
    current_user: CurrentUserDep,
    filter: Annotated[FilterUserSchema, Query()],
) -> dict:
    with UnitOfWork(session) as uow:
        return user_service_read_many(
            uow=uow, current_user=current_user, filter=filter
        )


@router.get(
    '/{user_id}', response_model=UserReadOneSchema, status_code=HTTPStatus.OK
)
def user_route_read_one(
    session: SessionDep,
    current_user: CurrentUserDep,
    user_id: UUID,
) -> UserModel:
    with UnitOfWork(session) as uow:
        return user_service_read_one(
            uow=uow,
            current_user=current_user,
            user_id=user_id,
        )


@router.get('/me', response_model=UserReadOneSchema, status_code=HTTPStatus.OK)
def user_route_read_me(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> UserModel:
    with UnitOfWork(session) as uow:
        return user_service_read_one(
            uow=uow,
            current_user=current_user,
            user_id=current_user.id,
        )
