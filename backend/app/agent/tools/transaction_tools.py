from datetime import date
from decimal import Decimal
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.models.account import Account
from app.models.transaction import Transaction, TransactionType
from langchain_core.tools import tool
from sqlalchemy import select,or_, String
from typing import Annotated
from langgraph.prebuilt import InjectedState


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
) -> str:
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
        return "Amount must be greater than zero."

    # amount = Decimal(str(amount))

    # -----------------------------
    # Validate Transaction Type
    # -----------------------------
    try:
        transaction_type = TransactionType(transaction_type.upper())
    except ValueError:
        return (
            f"Invalid transaction type. "
            f"Allowed values: {[t.value for t in TransactionType]}"
        )

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
                return "Account not found or does not belong to the user."

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
                    return "Insufficient balance."

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

            return (
                f"Transaction created successfully.\n\n"
                f"Transaction ID : {transaction.id}\n"
                f"Type           : {transaction.transaction_type.value}\n"
                f"Amount         : ₹{transaction.amount}\n"
                f"Balance        : ₹{account.balance}"
            )

        except Exception as e:
            await db.rollback()
            return f"Error creating transaction: {str(e)}"

# ---------------------------------------------------------------------------
# Tool 2: list_transaction
# ---------------------------------------------------------------------------
@tool("list_transactions")
async def list_transactions(
    user_id: Annotated[str, InjectedState("user_id")],
    account_id: UUID | None = None,
    transaction_type: str | None = None,
) -> str:
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
            if account_id:
                query = query.where(Transaction.account_id == account_id)

            # Filter by transaction type
            if transaction_type:
                try:
                    transaction_type = TransactionType(transaction_type.upper())
                except ValueError:
                    return (
                        f"Invalid transaction type. "
                        f"Allowed values: {[t.value for t in TransactionType]}"
                    )

                query = query.where(Transaction.transaction_type == transaction_type)

            # Latest first
            query = query.order_by(Transaction.transaction_date.desc())

            result = await db.execute(query)

            transactions = result.scalars().all()

            if not transactions:
                return "No transactions found."

            response = ["Transactions:\n"]

            for tx in transactions:
                response.append(
                    f"""
ID          : {tx.id}
Amount      : ₹{tx.amount}
Type        : {tx.transaction_type.value}
Description : {tx.description or "N/A"}
Date        : {tx.transaction_date}
Account ID  : {tx.account_id}
------------------------------
""".strip()
                )

            return "\n".join(response)

        except Exception as e:
            return f"Error listing transactions: {str(e)}"
        

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
) -> str:
    """
    Update an existing transaction.
    """

    async with AsyncSessionLocal() as db:
        try:
            # Get transaction
            result = await db.execute(
                select(Transaction).where(
                    Transaction.id == transaction_id,
                    Transaction.user_id == user_id,
                )
            )

            transaction = result.scalar_one_or_none()

            if transaction is None:
                return "Transaction not found."

            # Get account
            account = await db.get(Account, transaction.account_id)

            if account is None:
                return "Associated account not found."

            # ------------------------------------
            # Reverse old transaction effect
            # ------------------------------------
            if transaction.transaction_type == TransactionType.INCOME:
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount

            # ------------------------------------
            # Update fields
            # ------------------------------------

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
                    return (
                        f"Invalid transaction type. "
                        f"Allowed values: {[t.value for t in TransactionType]}"
                    )

            # ------------------------------------
            # Apply new transaction effect
            # ------------------------------------

            if new_type == TransactionType.INCOME:
                account.balance += new_amount
            else:
                if account.balance < new_amount:
                    return "Insufficient balance."

                account.balance -= new_amount

            # ------------------------------------
            # Update transaction
            # ------------------------------------

            transaction.amount = new_amount
            transaction.transaction_type = new_type

            if description is not None:
                transaction.description = description

            if transaction_date is not None:
                transaction.transaction_date = transaction_date

            await db.commit()
            await db.refresh(transaction)

            return (
                f"Transaction updated successfully.\n\n"
                f"Transaction ID : {transaction.id}\n"
                f"Amount         : ₹{transaction.amount}\n"
                f"Type           : {transaction.transaction_type.value}\n"
                f"Balance        : ₹{account.balance}"
            )

        except Exception as e:
            await db.rollback()
            return f"Error updating transaction: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 4: Delete Transaction
# ---------------------------------------------------------------------------
@tool("delete_transaction")
async def delete_transaction(
    transaction_id: UUID,
    user_id: Annotated[str, InjectedState("user_id")],
) -> str:
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
                return "Transaction not found."

            account = await db.get(Account, transaction.account_id)

            if account is None:
                return "Associated account not found."

            # Reverse transaction effect
            if transaction.transaction_type == TransactionType.INCOME:
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount

            await db.delete(transaction)

            await db.commit()

            return (
                f"Transaction deleted successfully.\n\n"
                f"Transaction ID : {transaction.id}\n"
                f"Current Balance: ₹{account.balance}"
            )

        except Exception as e:
            await db.rollback()
            return f"Error deleting transaction: {str(e)}"


# ---------------------------------------------------------------------------
# Tool 5: Search Transaction
# ---------------------------------------------------------------------------

@tool("search_transactions")
async def search_transactions(
    user_id: Annotated[str, InjectedState("user_id")],
    keyword: str,
) -> str:
    """
    Search transactions using description or transaction type.
    """

    async with AsyncSessionLocal() as db:
        try:
            query = select(Transaction).where(
                Transaction.user_id == user_id,
                or_(
                    Transaction.description.ilike(f"%{keyword}%"),
                    Transaction.transaction_type.cast(String).ilike(f"%{keyword}%"),
                ),
            ).order_by(Transaction.transaction_date.desc())

            result = await db.execute(query)

            transactions = result.scalars().all()

            if not transactions:
                return "No matching transactions found."

            response = ["Matching Transactions:\n"]

            for tx in transactions:
                response.append(
                    f"""
ID          : {tx.id}
Amount      : ₹{tx.amount}
Type        : {tx.transaction_type.value}
Description : {tx.description or "N/A"}
Date        : {tx.transaction_date}
Account ID  : {tx.account_id}
------------------------------
""".strip()
                )

            return "\n".join(response)

        except Exception as e:
            return f"Error searching transactions: {str(e)}"