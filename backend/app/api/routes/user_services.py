from app.core.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schema.user_services import (
    AccountResponse,
    GetUserAccountsResponse,
    GetUserTransactionsResponse,
    TransactionResponse,
)
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/service", tags=["User related services"])


@router.get("/accounts", response_model=GetUserAccountsResponse)
async def get_user_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(
            Account.id,
            Account.name,
            Account.balance,
            Account.account_type,
        ).where(Account.user_id == current_user.id)
    )

    accounts = [AccountResponse(**row) for row in result.mappings().all()]

    return GetUserAccountsResponse(accounts=accounts)


@router.get("/transactions", response_model=GetUserTransactionsResponse)
async def get_user_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(
            Transaction.id,
            Transaction.amount,
            Transaction.transaction_type,
            Transaction.description,
            Transaction.transaction_date,
            Transaction.account_id,
        ).where(Transaction.user_id == current_user.id)
    )

    transactions = [TransactionResponse(**row) for row in result.mappings().all()]

    return GetUserTransactionsResponse(transactions=transactions)
