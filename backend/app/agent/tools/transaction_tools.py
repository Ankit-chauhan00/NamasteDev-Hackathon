from datetime import date
from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.models.account import Account
from app.models.transaction import Transaction, TransactionType
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from sqlalchemy import String, or_, select


# ---------------------------------------------------------------------------
# Tool 1: create_transaction
# ---------------------------------------------------------------------------
@tool("create_transaction")
async def create_transaction(
    user_id: Annotated[str, InjectedState("user_id")],
    account_name: str,
    amount: Decimal,
    transaction_type: str,
    description: str | None = None,
    transaction_date: date | None = None,
) -> dict[str, Any]:
    """
    Create a financial transaction for a user's account.

    Transaction Types:
    - INCOME   -> Adds to account balance
    - EXPENSE  -> Deducts from account balance
    - TRANSFER -> Deducts from account balance
    """

    # -----------------------------
    # Validate Amount
    # -----------------------------
    if amount <= 0:
        return {"status": False, "message": "Amount must be greater than zero."}

    # amount = Decimal(str(amount))

    # -----------------------------
    # Validate Transaction Type
    # -----------------------------
    try:
        transaction_type = TransactionType(transaction_type.upper())
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
        }

    if transaction_date is None:
        transaction_date = date.today()

    async with AsyncSessionLocal() as db:
        try:
            # -----------------------------
            # Verify Account
            # -----------------------------
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
                    "message": "Account not found or does not belong to the user.",
                }

            account_id = account.id

            # -----------------------------
            # Update Account Balance
            # -----------------------------
            if transaction_type == TransactionType.INCOME:
                account.balance += amount

            elif transaction_type in (
                TransactionType.EXPENSE,
                TransactionType.TRANSFER,
            ):
                if account.balance < amount:
                    return {"status": False, "message": "Insufficient balance."}

                account.balance -= amount

            # -----------------------------
            # Create Transaction
            # -----------------------------
            transaction = Transaction(
                account_id=account_id,
                user_id=user_id,
                amount=amount,
                transaction_type=transaction_type,
                description=description,
                transaction_date=transaction_date,
            )

            db.add(transaction)

            await db.commit()
            await db.refresh(transaction)

            return {
                "success": True,
                "message": "Transaction created successfully.",
                "transaction": {
                    "id": str(transaction.id),
                    "amount": float(transaction.amount),
                    "type": transaction.transaction_type.value,
                    "description": transaction.description,
                    "date": transaction.transaction_date.isoformat(),
                    "account_id": str(transaction.account_id),
                },
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }


# ---------------------------------------------------------------------------
# Tool 2: list_transaction
# ---------------------------------------------------------------------------
@tool("list_transactions")
async def list_transactions(
    user_id: Annotated[str, InjectedState("user_id")],
    account_id: UUID | None = None,
    transaction_type: str | None = None,
) -> dict[str, Any]:
    """
    List all transactions for a user.

    Optional Filters:
    - account_id
    - transaction_type (INCOME, EXPENSE, TRANSFER)
    """

    async with AsyncSessionLocal() as db:
        try:
            query = select(Transaction).where(Transaction.user_id == user_id)

            # Filter by account
            if account_id is not None:
                query = query.where(Transaction.account_id == account_id)

            # Filter by transaction type
            if transaction_type is not None:
                try:
                    transaction_type_enum = TransactionType(transaction_type.upper())
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid transaction type. Allowed values: {[t.value for t in TransactionType]}",
                    }

                query = query.where(
                    Transaction.transaction_type == transaction_type_enum
                )

            query = query.order_by(Transaction.transaction_date.desc())

            result = await db.execute(query)
            transactions = result.scalars().all()

            if not transactions:
                return {
                    "success": False,
                    "message": "No transactions found.",
                }

            return {
                "success": True,
                "count": len(transactions),
                "transactions": [
                    {
                        "id": str(tx.id),
                        "account_id": str(tx.account_id),
                        "amount": float(tx.amount),
                        "transaction_type": tx.transaction_type.value,
                        "description": tx.description,
                        "transaction_date": tx.transaction_date.isoformat(),
                    }
                    for tx in transactions
                ],
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }
# ---------------------------------------------------------------------------
# Tool 3: update_transaction
# ---------------------------------------------------------------------------
@tool("update_transaction")
async def update_transaction(
    transaction_id: UUID,
    user_id: Annotated[str, InjectedState("user_id")],
    amount: Decimal | None = None,
    transaction_type: str | None = None,
    description: str | None = None,
    transaction_date: date | None = None,
) -> dict[str, Any]:
    """
    Update an existing transaction.
    """

    async with AsyncSessionLocal() as db:
        try:
            # -----------------------------
            # Get Transaction
            # -----------------------------
            result = await db.execute(
                select(Transaction).where(
                    Transaction.id == transaction_id,
                    Transaction.user_id == user_id,
                )
            )

            transaction = result.scalar_one_or_none()

            if transaction is None:
                return {
                    "success": False,
                    "message": "Transaction not found.",
                }

            # -----------------------------
            # Get Associated Account
            # -----------------------------
            account = await db.get(Account, transaction.account_id)

            if account is None:
                return {
                    "success": False,
                    "message": "Associated account not found.",
                }

            # -----------------------------
            # Reverse Old Transaction Effect
            # -----------------------------
            if transaction.transaction_type == TransactionType.INCOME:
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount

            # -----------------------------
            # New Values
            # -----------------------------
            new_amount = (
                Decimal(str(amount))
                if amount is not None
                else transaction.amount
            )

            new_type = transaction.transaction_type

            if transaction_type is not None:
                try:
                    new_type = TransactionType(transaction_type.upper())
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid transaction type. Allowed values: {[t.value for t in TransactionType]}",
                    }

            # -----------------------------
            # Apply New Effect
            # -----------------------------
            if new_type == TransactionType.INCOME:
                account.balance += new_amount
            else:
                if account.balance < new_amount:
                    return {
                        "success": False,
                        "message": "Insufficient balance.",
                    }

                account.balance -= new_amount

            # -----------------------------
            # Update Transaction
            # -----------------------------
            transaction.amount = new_amount
            transaction.transaction_type = new_type

            if description is not None:
                transaction.description = description

            if transaction_date is not None:
                transaction.transaction_date = transaction_date

            await db.commit()
            await db.refresh(transaction)
            await db.refresh(account)

            return {
                "success": True,
                "message": "Transaction updated successfully.",
                "transaction": {
                    "id": str(transaction.id),
                    "account_id": str(transaction.account_id),
                    "amount": float(transaction.amount),
                    "transaction_type": transaction.transaction_type.value,
                    "description": transaction.description,
                    "transaction_date": transaction.transaction_date.isoformat(),
                },
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }

# ---------------------------------------------------------------------------
# Tool 4: Delete Transaction
# ---------------------------------------------------------------------------
@tool("delete_transaction")
async def delete_transaction(
    transaction_id: UUID,
    user_id: Annotated[str, InjectedState("user_id")],
) -> dict[str, Any]:
    """
    Delete a transaction and restore the account balance.
    """

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Transaction).where(
                    Transaction.id == transaction_id,
                    Transaction.user_id == user_id,
                )
            )

            transaction = result.scalar_one_or_none()

            if transaction is None:
                return {
                    "success": False,
                    "message": "Transaction not found.",
                }

            account = await db.get(Account, transaction.account_id)

            if account is None:
                return {
                    "success": False,
                    "message": "Associated account not found.",
                }

            # Reverse transaction effect
            if transaction.transaction_type == TransactionType.INCOME:
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount

            deleted_transaction = {
                "id": str(transaction.id),
                "amount": float(transaction.amount),
                "transaction_type": transaction.transaction_type.value,
                "description": transaction.description,
                "transaction_date": transaction.transaction_date.isoformat(),
                "account_id": str(transaction.account_id),
            }

            await db.delete(transaction)
            await db.commit()

            return {
                "success": True,
                "message": "Transaction deleted successfully.",
                "deleted_transaction": deleted_transaction,
                "account": {
                    "id": str(account.id),
                    "name": account.name,
                    "balance": float(account.balance),
                },
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": str(e),
            }

# ---------------------------------------------------------------------------
# Tool 5: Search Transaction
# ---------------------------------------------------------------------------
@tool("search_transactions")
async def search_transactions(
    user_id: Annotated[str, InjectedState("user_id")],
    keyword: str,
) -> dict[str, Any]:
    """
    Search transactions using description or transaction type.
    """

    async with AsyncSessionLocal() as db:
        try:
            query = (
                select(Transaction)
                .where(
                    Transaction.user_id == user_id,
                    or_(
                        Transaction.description.ilike(f"%{keyword}%"),
                        Transaction.transaction_type.cast(String).ilike(f"%{keyword}%"),
                    ),
                )
                .order_by(Transaction.transaction_date.desc())
            )

            result = await db.execute(query)
            transactions = result.scalars().all()

            if not transactions:
                return {
                    "success": False,
                    "message": "No matching transactions found.",
                }

            return {
                "success": True,
                "count": len(transactions),
                "transactions": [
                    {
                        "id": str(tx.id),
                        "account_id": str(tx.account_id),
                        "amount": float(tx.amount),
                        "transaction_type": tx.transaction_type.value,
                        "description": tx.description,
                        "transaction_date": tx.transaction_date.isoformat(),
                    }
                    for tx in transactions
                ],
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }