from uuid import UUID

from TS_TP.core.security import get_password_hash
from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.user.user_exc import UserNotFound
from TS_TP.domain.user.user_models import UserModel
from TS_TP.domain.user.user_schemas import (
    FilterUserSchema,
    UserCreateSchema,
    UserReadManySchema,
)


def user_service_create(
    *, uow: UnitOfWork, current_user: UserModel, data: UserCreateSchema
) -> UserModel:
    password_hash = get_password_hash(data.password)

    new_user = UserModel(
        email=data.email,
        password_hash=password_hash,
        name=data.name,
        role=data.role,
    )

    return uow.users.add(new_user)


def user_service_read_many(
    *, uow: UnitOfWork, current_user: UserModel, filter: FilterUserSchema
) -> UserReadManySchema:
    users, total = uow.users.get_many(filter)

    return {
        'users': users,
        'total': total,
        'offset': filter.offset,
        'limit': filter.limit,
    }


def user_service_read_one(
    *, uow: UnitOfWork, current_user: UserModel, user_id: UUID
) -> UserModel:
    user = uow.users.get_one(user_id)

    if not user:
        raise UserNotFound()
    else:
        return user
