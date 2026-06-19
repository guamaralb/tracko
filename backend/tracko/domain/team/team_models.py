from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from tracko.core.database import table_registry
from tracko.domain.user_team.user_team_models import UserTeamModel


@mapped_as_dataclass(table_registry)
class TeamModel:
    __tablename__ = 'teams'

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id_creator: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )

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

    # Relationships
    user_creator: Mapped['UserModel'] = relationship(  # noqa: F821
        'UserModel',
        foreign_keys=[user_id_creator],
        back_populates='teams_created',
        init=False,
    )

    users_attributed: Mapped[list['UserModel']] = relationship(  # noqa: F821
        'UserModel',
        secondary=UserTeamModel.__table__,
        back_populates='teams_attributed',
        init=False,
    )
