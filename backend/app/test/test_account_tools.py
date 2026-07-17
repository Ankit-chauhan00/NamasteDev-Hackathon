import asyncio
from uuid import UUID

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.account import Account
from app.agent.tools.account_tools import (
    create_account,
    list_user_account,
    get_account_balance,
    update_account,
    delete_account,
)

USER_ID = UUID("12192fd2-1746-4cb0-a02a-223ee473a95a")


async def get_account_id(name: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Account).where(
                Account.user_id == USER_ID,
                Account.name == name,
            )
        )

        account = result.scalar_one_or_none()

        if account is None:
            return None

        return account.id


async def main():

    # -------------------------------
    # Create Account
    # -------------------------------
    print("\n========== CREATE ACCOUNT ==========")

    result = await create_account.ainvoke(
        {
            "user_id": USER_ID,
            "name": "Axis Salary",
            "balance": 25000,
            "account_type": "CURRENT",
        }
    )

    print(result)

    # -------------------------------
    # List Accounts
    # -------------------------------
    print("\n========== LIST ACCOUNTS ==========")

    result = await list_user_account.ainvoke(
        {
            "user_id": USER_ID,
        }
    )

    print(result)

    # -------------------------------
    # Fetch Account ID
    # -------------------------------
    account_id = await get_account_id("Axis Salary")

    if account_id is None:
        print("Could not find account.")
        return

    print("\nAccount ID:", account_id)

    # -------------------------------
    # Get Balance
    # -------------------------------
    print("\n========== GET BALANCE ==========")

    result = await get_account_balance.ainvoke(
        {
            "user_id": USER_ID,
            "account_id": account_id,
            "name": "hdfc"
        }
    )

    print(result)

    # -------------------------------
    # Update Account
    # -------------------------------
    print("\n========== UPDATE ACCOUNT ==========")

    result = await update_account.ainvoke(
        {
            "user_id": USER_ID,
            "account_id": account_id,
            "name": "Axis Updated",
            "balance": 50000,
            "account_type": "SAVINGS",
        }
    )

    print(result)

    # -------------------------------
    # Get Balance Again
    # -------------------------------
    print("\n========== GET UPDATED ACCOUNT ==========")

    result = await get_account_balance.ainvoke(
        {
            "user_id": USER_ID,
            "account_id": account_id,
        }
    )

    print(result)

    # -------------------------------
    # Delete Account
    # -------------------------------
    print("\n========== DELETE ACCOUNT ==========")

    result = await delete_account.ainvoke(
        {
            "user_id": USER_ID,
            "account_id": account_id,
        }
    )

    print(result)

    # -------------------------------
    # Final List
    # -------------------------------
    print("\n========== FINAL ACCOUNT LIST ==========")

    result = await list_user_account.ainvoke(
        {
            "user_id": USER_ID,
        }
    )

    print(result)


asyncio.run(main())