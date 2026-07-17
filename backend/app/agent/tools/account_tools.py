from decimal import Decimal
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.models.account import Account, AccountType
from langchain_core.tools import tool
from sqlalchemy import select

# ---------------------------------------------------------------------------
# Tool 1: create_account
# ---------------------------------------------------------------------------


@tool("create_account")
async def create_account(
    user_id: UUID, name: str, balance: float, account_type: str = "CURRENT"
) -> str:
    """
    Create a new account for the authenticated user.
    """

    

    # Validate account type
    try:
        account_type_enum = AccountType(account_type.upper())
    except ValueError:
        return f"Invalid account type. Allowed values: {[e.value for e in AccountType]}"

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
                return f"An account named '{name}' already exists."
            if balance is not None and balance < 0:
                return "Balance cannot be negative."

            account = Account(
                name=name,
                balance=Decimal(str(balance)),
                account_type=account_type_enum,
                user_id=user_id,
            )

            db.add(account)

            await db.commit()
            await db.refresh(account)

            return (
                f"Account created successfully!\n\n"
                f"Name: {account.name}\n"
                f"Balance: ₹{account.balance}\n"
                f"Type: {account.account_type.value}"
            )

        except Exception as e:
            await db.rollback()
            return f"Failed to create account: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 2: list all the accounts
# ---------------------------------------------------------------------------


@tool("list_accounts")
async def list_user_account(user_id: UUID) -> str:
    """List the all account user have"""

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
                return "No Account found for this user."

            response = ["Your accounts:\n"]

            for account in accounts:
                response.append(
                    f"- {account.name} "
                    f"({account.account_type.value}) "
                    f": ₹{account.balance}"
                )

            return "\n".join(response)

        except Exception as e:
            return f"Failed to fetch accounts: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 3: Get Account Balance
# ---------------------------------------------------------------------------


@tool("get_account_balance")
async def get_account_balance(
    user_id: UUID, account_id: UUID | None = None, account_name: str | None = None
) -> str:
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
                return "please provide either account_id or account_name."

            account = result.scalar_one_or_none()

            if account is None:
                return "Account not found."

            return (
                f"Account: {account.name}\n"
                f"Type: {account.account_type.value}\n"
                f"Current Balance: ₹{account.balance}"
            )

        except Exception as e:
            return f"Failed to fetch account balance: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 4: update account or change the account
# ---------------------------------------------------------------------------


@tool("update_account")
async def update_account(
    user_id: UUID,
    account_id: UUID,
    name: str | None = None,
    balance: float | None = None,
    account_type: str | None = None,
) -> str:
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
                return "Account not found."

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
                except ValueError:
                    return (
                        "Invalid account type. "
                        f"Allowed values: {[e.value for e in AccountType]}"
                    )

            await db.commit()
            await db.refresh(account)

            return (
                "Account updated successfully!\n\n"
                f"Name: {account.name}\n"
                f"Balance: ₹{account.balance}\n"
                f"Type: {account.account_type.value}"
            )

        except Exception as e:
            await db.rollback()
            return f"Failed to update account: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 5: delete account
# ---------------------------------------------------------------------------


@tool("delete_account")
async def delete_account(
    user_id: UUID,
    account_id: UUID | None = None,
    account_name: str | None = None,
) -> str:
    """
    Delete one of the authenticated user's accounts using either the
    account ID or the account name.
    """

    if account_id is None and account_name is None:
        return "Please provide either an account ID or an account name."

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
                return "Account not found."

            await db.delete(account)
            await db.commit()

            return f"Account '{account.name}' has been deleted successfully."

        except Exception as e:
            await db.rollback()
            return f"Failed to delete account: {str(e)}"
