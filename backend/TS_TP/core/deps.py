from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from TS_TP.core.database import get_session

# from TS_TP.domain.users.models import UserModel

SessionDep = Annotated[Session, Depends(get_session)]
# CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
