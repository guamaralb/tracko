from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    String,
    Text,
    Uuid,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from TS_TP.core.database import table_registry
from TS_TP.domain.task.task_enums import TaskStatusEnum


@mapped_as_dataclass(table_registry)
class TaskModel:
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), init=False, primary_key=True, default_factory=uuid4
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    description: Mapped[str] = mapped_column(Text, nullable=True)

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[TaskStatusEnum] = mapped_column(
        SAEnum(TaskStatusEnum, values_callable=lambda e: [i.value for i in e]),
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
