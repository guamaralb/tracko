from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserReadSchema(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListReadSchema(BaseModel):
    users: list[UserReadSchema]
    total: int


class UserPatchSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None
