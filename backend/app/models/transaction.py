"""As user will place transaction"""
from enum import Enum
from decimal import Decimal
from datetime import date

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  String ,Enum as SQLEnum, ForeignKey, Numeric, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.account import Account

class TransactionType(str,Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"


class Transaction(BaseModel):
    __tablename__= "transactions"

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        nullable=False,
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type_enum"),
        default=TransactionType.EXPENSE,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    account: Mapped["Account"]= mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    account: Mapped["Account"] = relationship(
        back_populates="transactions",
    )
    
    user: Mapped["User"] = relationship(
        back_populates="transactions",
    )
        
