from sqlalchemy import select

from tracko.core.deps import SessionDep
from tracko.core.security import get_password_hash
from tracko.core.settings import settings
from tracko.domain.user.user_enums import UserRoleEnum
from tracko.domain.user.user_models import UserModel


def seed_first_admin_user(session: SessionDep):
    print('-- Running Seed: first_admin_user --')

    db_user = session.scalar(
        select(UserModel).where(
            UserModel.email == settings.FIRST_ADMIN_USER_EMAIL
        )
    )

    if db_user:
        print(f'User {db_user.email} already exists. Skipping.')
        user = db_user

    else:
        user = UserModel(
            email=settings.FIRST_ADMIN_USER_EMAIL,
            name=settings.FIRST_ADMIN_USER_NAME,
            role=UserRoleEnum.ADMIN,
            password_hash=get_password_hash(
                settings.FIRST_ADMIN_USER_password
            ),
        )
        session.add(user)
        session.flush()

        print(f'User {user.email} added.')
