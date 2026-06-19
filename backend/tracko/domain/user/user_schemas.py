from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from tracko.domain.shared.shared_schemas import FilterPageSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserReadOneSchema(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserReadManySchema(BaseModel):
    users: list[UserReadOneSchema]
    total: int
    offset: int
    limit: int


class UserPatchSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None


class FilterUserSchema(FilterPageSchema):
    name: str | None = None
    email: str | None = None
    is_active: bool | None = None
