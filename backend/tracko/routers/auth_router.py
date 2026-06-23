from fastapi import APIRouter, HTTPException, status

from tracko.core.deps import OAuth2FormDep, SessionDep
from tracko.domain.auth.auth_exc import WrongCredentials
from tracko.domain.auth.auth_schemas import TokenSchema
from tracko.domain.auth.auth_services import (
    login_for_access_token_service,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
def login_for_access_token(
    form_data: OAuth2FormDep, session: SessionDep
) -> TokenSchema:
    try:
        return login_for_access_token_service(
            form_data=form_data, session=session
        )
    except WrongCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas. Verifique seu usuário e senha.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
