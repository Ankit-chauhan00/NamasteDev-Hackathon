"""Goal model for tracking user's financial goals."""

import enum
from datetime import  datetime

from sqlalchemy import String, DateTime, Text, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING

from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class GoalPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GoalStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# no need to create id and created At as defined in baseModel
class Goal(BaseModel):
    __tablename__ = "goals"

    title: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    target_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    current_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    priority: Mapped[GoalPriority] = mapped_column(
        SQLEnum(GoalPriority),
        default=GoalPriority.MEDIUM,
        nullable=False,
    )

    status: Mapped[GoalStatus] = mapped_column(
        SQLEnum(GoalStatus),
        default=GoalStatus.ACTIVE,
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship(
        "User",
        back_populates="goals",
    )
