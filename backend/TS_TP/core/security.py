from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from TS_TP.core.core_exc import InvalidToken
from TS_TP.core.database import get_session
from TS_TP.core.settings import settings
from TS_TP.domain.user.user_models import UserModel

password_context = PasswordHash.recommended()


def craete_access_token(data: dict) -> str:
    to_encode = data.copy()
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh_token'
)


def get_current_user(
    # Dependency must be explicit since this function is called in core.deps
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> UserModel:
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')

        if not subject_email:
            raise InvalidToken()

    except DecodeError:
        raise InvalidToken()

    except ExpiredSignatureError:
        raise InvalidToken()

    db_user = session.scalar(
        select(UserModel).where(UserModel.email == subject_email)
    )

    return db_user
