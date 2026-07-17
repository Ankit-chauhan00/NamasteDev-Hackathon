"""It defines about the account of the user as a user can have multiple account"""


from decimal import Decimal

from sqlalchemy import  Numeric,ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING
from enum import Enum

from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction


class AccountType(str, Enum):
     SAVINGS = "SAVINGS"
     CURRENT = "CURRENT"


class Account(BaseModel):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
        nullable=False
    )

    account_type: Mapped[AccountType] = mapped_column(
        SQLEnum(AccountType, name="account_type_enum"),
        default=AccountType.SAVINGS,
        nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="accounts",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
    back_populates="account",
    cascade="all, delete-orphan",
    )