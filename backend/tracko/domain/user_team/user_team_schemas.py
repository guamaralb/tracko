from uuid import UUID

from tracko.domain.shared.shared_schemas import FilterPageSchema
from tracko.domain.user.user_enums import UserRoleEnum


class FilterUserTeamSchema(FilterPageSchema):
    user_id: UUID | None = None
    team_id: UUID | None = None
    role: UserRoleEnum | None = None
