from sqlalchemy import select

from TS_TP.core.deps import SessionDep
from TS_TP.core.security import craete_access_token, verify_password
from TS_TP.domain.auth.auth_exc import WrongCredentials
from TS_TP.domain.auth.auth_schemas import TokenSchema
from TS_TP.domain.user.user_exc import UserNotActive
from TS_TP.domain.user.user_models import UserModel


def login_for_access_token_service(
    form_data, session: SessionDep
) -> TokenSchema:
    db_user = session.scalar(
        select(UserModel).where(UserModel.email == form_data.username)
    )

    if not db_user:
        raise WrongCredentials()

    if not db_user.is_active:
        raise UserNotActive()

    if not verify_password(form_data.password, db_user.password_hash):
        raise WrongCredentials()

    access_token = craete_access_token(data={'sub': db_user.email})

    complete_token = TokenSchema(
        access_token=access_token, token_type='bearer'
    )

    return complete_token
