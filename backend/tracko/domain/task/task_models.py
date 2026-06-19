from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from tracko.core.database import table_registry
from tracko.domain.task.task_enums import TaskStatusEnum
from tracko.domain.users_tasks.users_tasks_models import UserTaskModel


@mapped_as_dataclass(table_registry)
class TaskModel:
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    user_id_creator: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )

    description: Mapped[str] = mapped_column(Text, nullable=True)

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[TaskStatusEnum] = mapped_column(
        Enum(TaskStatusEnum, values_callable=lambda e: [i.value for i in e]),
        nullable=False,
        default=TaskStatusEnum.TODO,
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
        back_populates='tasks_created',
        init=False,
    )

    users_attributed: Mapped[list['UserModel']] = relationship(  # noqa: F821
        'UserModel',
        secondary=UserTaskModel.__table__,
        back_populates='tasks_attributed',
        init=False,
    )
