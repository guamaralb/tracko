from uuid import UUID

from TS_TP.core.uow import UnitOfWork
from TS_TP.domain.user.user_exc import UserNotFound
from TS_TP.domain.user.user_models import UserModel
from TS_TP.domain.user.user_schemas import UserCreateSchema


def user_service_create(*, uow: UnitOfWork, data: UserCreateSchema) -> UserModel:
    pwd_hash = data.password  # CORRIGIR

    new_user = UserModel(email=data.email, pwd_hash=pwd_hash, name=data.name)

    return uow.users.add(new_user)


def user_service_read_one(*, uow: UnitOfWork, user_id: UUID) -> UserModel:
    user = uow.users.get_one(user_id)

    if not user:
        raise UserNotFound()
    else:
        return user
