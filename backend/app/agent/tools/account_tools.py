from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.models.account import Account, AccountType
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from sqlalchemy import select

# ---------------------------------------------------------------------------
# Tool 1: create_account
# ---------------------------------------------------------------------------


@tool("create_account")
async def create_account(
    user_id: Annotated[str, InjectedState("user_id")],
    name: str,
    balance: float,
    account_type: str = "CURRENT",
) -> dict[str, Any]:
    """
    Create a new account for the authenticated user.
    """

    # Validate account type
    try:
        account_type_enum = AccountType(account_type.upper())
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
        }

    async with AsyncSessionLocal() as db:
        try:
            # Check if an account with the same name already exists
            result = await db.execute(
                select(Account).where(
                    Account.user_id == user_id, Account.name.ilike(f"{name}")
                )
            )

            existing_account = result.scalar_one_or_none()

            if existing_account:
                return {"success": False, "message": "Account alredy exists"}
            if balance is not None and balance < 0:
                return {"success": False, "message": "Balance cannot be negative."}

            account = Account(
                name=name,
                balance=Decimal(str(balance)),
                account_type=account_type_enum,
                user_id=user_id,
            )

            db.add(account)

            await db.commit()
            await db.refresh(account)

            return {
                "success": True,
                "message": "Account created successfully.",
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                    "account_type": account.account_type.value,
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }


# ---------------------------------------------------------------------------
# Tool 2: list all the accounts
# ---------------------------------------------------------------------------


@tool("list_accounts")
async def list_user_account(
    user_id: Annotated[str, InjectedState("user_id")],
) -> dict[str, Any]:
    """
    List all accounts belonging to the authenticated user.

    Use this tool only when the user asks to:
    - view their accounts
    - know available accounts
    - choose between accounts

    Do not call this tool before every transaction.
    """

    async with AsyncSessionLocal() as db:
        try:
            # get all the accounts user have
            result = await db.execute(
                select(Account)
                .where(Account.user_id == user_id)
                .order_by(Account.created_at)
            )

            accounts = result.scalars().all()

            if not accounts:
                return {
                    "success": False,
                    "message": "Account not found",
                }

            return {
                "success": True,
                "accounts": [
                    {
                        "id": str(account.id),
                        "name": account.name,
                        "balance": float(account.balance),
                        "account_type": account.account_type.value,
                    }
                    for account in accounts
                ],
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }


# ---------------------------------------------------------------------------
# Tool 3: Get Account Balance
# ---------------------------------------------------------------------------


@tool("get_account_balance")
async def get_account_balance(
    user_id: Annotated[str, InjectedState("user_id")],
    account_id: UUID | None = None,
    account_name: str | None = None,
) -> dict[str, Any]:
    """Get the balance of a specific account belonging to the authenticated user."""

    async with AsyncSessionLocal() as db:
        try:
            if account_id is not None:
                result = await db.execute(
                    select(Account).where(
                        Account.id == account_id,
                        Account.user_id == user_id,
                    )
                )
            elif account_name is not None:
                result = await db.execute(
                    select(Account).where(
                        Account.user_id == user_id,
                        Account.name.ilike(f"%{account_name}%"),
                    )
                )
            else:
                return {
                    "status": False,
                    "message": "please provide either account_id or account_name.",
                }

            account = result.scalar_one_or_none()

            if account is None:
                return {"status": False, "message": "Account not found"}

            return {
                "success": True,
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                    "account_type": account.account_type.value,
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }


# ---------------------------------------------------------------------------
# Tool 4: update account or change the account
# ---------------------------------------------------------------------------


@tool("update_account")
async def update_account(
    user_id: Annotated[str, InjectedState("user_id")],
    account_id: UUID,
    name: str | None = None,
    balance: float | None = None,
    account_type: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing account's name, balance, or account type.
    """

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Account).where(
                    Account.id == account_id,
                    Account.user_id == user_id,
                )
            )

            account = result.scalar_one_or_none()

            if account is None:
                return {"status": False, "message": "Account Not Found"}

            # Update name
            if name is not None:
                account.name = name

            # Update balance
            if balance is not None:
                account.balance = Decimal(str(balance))

            # Update account type
            if account_type is not None:
                try:
                    account.account_type = AccountType(account_type.upper())
                except ValueError as e:
                    return {
                        "success": False,
                        "message": str(e),
                    }

            await db.commit()
            await db.refresh(account)

            return {
                "success": True,
                "message": "Account updated successfully.",
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                    "account_type": account.account_type.value,
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }


# ---------------------------------------------------------------------------
# Tool 5: delete account
# ---------------------------------------------------------------------------


@tool("delete_account")
async def delete_account(
    user_id: Annotated[str, InjectedState("user_id")],
    account_id: UUID | None = None,
    account_name: str | None = None,
) -> dict[str, Any]:
    """
    Delete one of the authenticated user's accounts using either the
    account ID or the account name.
    """

    if account_id is None and account_name is None:
        return {
            "status": False,
            "message": "Please provide either an account ID or an account name."
        }

    async with AsyncSessionLocal() as db:
        try:
            if account_id is not None:
                result = await db.execute(
                    select(Account).where(
                        Account.id == account_id,
                        Account.user_id == user_id,
                    )
                )
            else:
                result = await db.execute(
                    select(Account).where(
                        Account.user_id == user_id,
                        Account.name.ilike(f"%{account_name}%"),
                    )
                )

            account = result.scalar_one_or_none()

            if account is None:
                return {
                    "status": False,
                    "message": "Account not found"
                }

            await db.delete(account)
            await db.commit()

            return {
                "success": True,
                "message": "Account deleted successfully.",
                "deleted_account": {
                "id": str(account.id),
                "name": account.name,
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }
