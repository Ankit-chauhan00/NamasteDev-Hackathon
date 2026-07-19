from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: UUID
    name: str
    balance: Decimal
    account_type: str

    model_config = {"from_attributes": True}


class GetUserAccountsResponse(BaseModel):
    accounts: list[AccountResponse]


class TransactionResponse(BaseModel):
    id: UUID
    amount: Decimal
    transaction_type: str
    description: str
    transaction_date: date
    account_id: UUID


class GetUserTransactionsResponse(BaseModel):
    transactions: list[TransactionResponse]
