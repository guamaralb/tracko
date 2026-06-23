from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
)

from tracko.core.database import table_registry


@mapped_as_dataclass(table_registry)
class UserTaskModel:
    __tablename__ = 'users_tasks'

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4)
    # FK
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    task_id: Mapped[UUID] = mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)

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
    __table_args__ = (UniqueConstraint('user_id', 'task_id', name='uq_user_task'),)
