from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from tracko.domain.shared.shared_schemas import FilterPageSchema
from tracko.domain.user.user_enums import UserRoleEnum


class TeamCreateSchema(BaseModel):
    name: str
    description: str | None = None


class TeamReadOneSchema(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamReadManySchema(BaseModel):
    teams: list[TeamReadOneSchema]
    total: int
    offset: int
    limit: int


class TeamPatchSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class FilterTeamSchema(FilterPageSchema):
    name: str | None = None
    description: str | None = None


class TeamAddMemberSchema(BaseModel):
    user_id: UUID
    role: UserRoleEnum


class TeamMemberReadOneSchema(BaseModel):
    user_id: UUID
    team_id: UUID
    role: UserRoleEnum
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)
