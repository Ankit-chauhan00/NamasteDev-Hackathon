from uuid import UUID

from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.user import User
from app.models.transaction import Transaction,TransactionType


# ---------------------------------------------------------------------------
# Tool-1: get_account_summary
# ---------------------------------------------------------------------------
@tool("get_account_summary")
async def get_account_summary(
    db: AsyncSession,
    user_id: UUID,
):
    """
    Get a summary of all accounts belonging to a user, including
    total balance, highest balance account, lowest balance account,
    and account details.
    """

    # Check user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Fetch accounts
    result = await db.execute(
        select(Account).where(Account.user_id == user_id)
    )

    accounts = result.scalars().all()

    if not accounts:
        return {
            "success": True,
            "message": "No accounts found.",
            "summary": {
                "total_accounts": 0,
                "total_balance": 0,
                "accounts": []
            }
        }

    total_balance = sum(account.balance for account in accounts)

    highest_balance = max(accounts, key=lambda account: account.balance)
    lowest_balance = min(accounts, key=lambda account: account.balance)

    return {
        "success": True,
        "summary": {
            "total_accounts": len(accounts),
            "total_balance": total_balance,
            "highest_balance_account": {
                "name": highest_balance.name,
                "balance": highest_balance.balance,
            },
            "lowest_balance_account": {
                "name": lowest_balance.name,
                "balance": lowest_balance.balance,
            },
            "accounts": [
                {
                    "id": account.id,
                    "name": account.name,
                    "balance": account.balance,
                    "account_type": account.account_type.value,
                }
                for account in accounts
            ],
        },
    }


# ---------------------------------------------------------------------------
# Tool-2: get_income_summary
# ---------------------------------------------------------------------------
@tool("get_income_summary")
async def get_income_summary(
    db: AsyncSession,
    user_id: UUID,
):
    """
    Return an income summary for the user.
    """
    # Check user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Fetch income transactions
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.INCOME,
        )
    )

    incomes = result.scalars().all()

    if not incomes:
        return {
            "success": True,
            "message": "No income transactions found.",
            "summary": {
                "total_income": 0,
                "income_transactions": 0,
                "largest_income": 0,
                "average_income": 0,
                "recent_income": [],
            },
        }

    total_income = sum(t.amount for t in incomes)
    largest_income = max(t.amount for t in incomes)
    average_income = total_income / len(incomes)

    recent_income = sorted(
        incomes,
        key=lambda t: t.transaction_date,
        reverse=True,
    )[:5]

    return {
        "success": True,
        "summary": {
            "total_income": total_income,
            "income_transactions": len(incomes),
            "largest_income": largest_income,
            "average_income": average_income,
            "recent_income": [
                {
                    "amount": tx.amount,
                    "description": tx.description,
                    "date": tx.transaction_date,
                }
                for tx in recent_income
            ],
        },
    }



# ---------------------------------------------------------------------------
# Tool-3: get_expense_summary
# ---------------------------------------------------------------------------
@tool("get_expense_summary")
async def get_expense_summary(
    db: AsyncSession,
    user_id: UUID,
):
    """
    Return an expense summary for the user.
    """
    # Check user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Fetch expense transactions
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE,
        )
    )

    expenses = result.scalars().all()

    if not expenses:
        return {
            "success": True,
            "message": "No expense transactions found.",
            "summary": {
                "total_expense": 0,
                "expense_transactions": 0,
                "largest_expense": 0,
                "average_expense": 0,
                "recent_expenses": [],
            },
        }

    total_expense = sum(t.amount for t in expenses)
    largest_expense = max(t.amount for t in expenses)
    average_expense = total_expense / len(expenses)

    recent_expenses = sorted(
        expenses,
        key=lambda t: t.transaction_date,
        reverse=True,
    )[:5]

    return {
        "success": True,
        "summary": {
            "total_expense": total_expense,
            "expense_transactions": len(expenses),
            "largest_expense": largest_expense,
            "average_expense": average_expense,
            "recent_expenses": [
                {
                    "amount": tx.amount,
                    "description": tx.description,
                    "date": tx.transaction_date,
                }
                for tx in recent_expenses
            ],
        },
    }


# ---------------------------------------------------------------------------
# Tool-4: get_recent_transactions
# ---------------------------------------------------------------------------
@tool("get_recent_transactions")
async def get_recent_transactions(
    db: AsyncSession,
    user_id: UUID,
    limit: int = 10,
):
    """
    Return the user's most recent transactions.
    """
    # Check user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Fetch recent transactions
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date.desc())
        .limit(limit)
    )

    transactions = result.scalars().all()

    if not transactions:
        return {
            "success": True,
            "message": "No transactions found.",
            "transactions": []
        }

    return {
        "success": True,
        "message": f"Found {len(transactions)} recent transaction(s).",
        "transactions": [
            {
                "id": tx.id,
                "amount": tx.amount,
                "transaction_type": tx.transaction_type.value,
                "description": tx.description,
                "transaction_date": tx.transaction_date,
                "account_id": tx.account_id,
            }
            for tx in transactions
        ],
    }