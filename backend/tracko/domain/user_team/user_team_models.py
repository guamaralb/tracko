from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from tracko.core.database import table_registry
from tracko.domain.user.user_enums import UserRoleEnum


@mapped_as_dataclass(table_registry)
class UserTeamModel:
    __tablename__ = 'users_teams'

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4)
    # FK
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    team_id: Mapped[UUID] = mapped_column(ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum, values_callable=lambda e: [i.value for i in e]))

    # Verification
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __post_init__(self):
        self.modified_at = self.created_at

    # Restriction
    __table_args__ = (UniqueConstraint('user_id', 'team_id', name='uq_user_team'),)
