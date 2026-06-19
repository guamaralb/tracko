from fastapi import APIRouter

from tracko.core.deps import OAuth2FormDep, SessionDep
from tracko.domain.auth.auth_schemas import TokenSchema
from tracko.domain.auth.auth_services import (
    login_for_access_token_service,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
def login_for_access_token(
    form_data: OAuth2FormDep, session: SessionDep
) -> TokenSchema:
    return login_for_access_token_service(form_data=form_data, session=session)
