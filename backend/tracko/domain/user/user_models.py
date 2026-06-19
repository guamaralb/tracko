from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, String, Uuid
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from tracko.core.database import table_registry
from tracko.domain.user.user_enums import UserRoleEnum
from tracko.domain.users_tasks.users_tasks_models import UserTaskModel


@mapped_as_dataclass(table_registry)
class UserModel:
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, values_callable=lambda e: [i.value for i in e])
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, init=False, default=True, nullable=False
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
    tasks_created: Mapped[list['TaskModel']] = relationship(  # noqa: F821
        'TaskModel',
        foreign_keys='TaskModel.user_id_creator',
        back_populates='user_creator',
        init=False,
    )

    tasks_attributed: Mapped[list['TaskModel']] = relationship(  # noqa: F821
        'TaskModel',
        secondary=UserTaskModel.__table__,
        back_populates='users_attributed',
        init=False,
    )
