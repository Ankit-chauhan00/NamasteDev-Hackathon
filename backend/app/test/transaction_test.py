from decimal import Decimal

from app.agent.tools.transaction_tools import (
    create_transaction,
    list_transactions,
    update_transaction,
    delete_transaction,
    search_transactions,
)

# ------------------------------------------------------------
# Replace these IDs with IDs from your database
# ------------------------------------------------------------
USER_ID = "12192fd2-1746-4cb0-a02a-223ee473a95a"
ACCOUNT_ID = "8f120a8f-2355-49f6-bb3f-0acc08bc7cfd"

# This will be filled after creation
TRANSACTION_ID = None


async def test_create():
    global TRANSACTION_ID

    print("\n========== CREATE TRANSACTION ==========")

    result = await create_transaction.ainvoke(
        {
            "account_id": ACCOUNT_ID,
            "user_id": USER_ID,
            "amount": Decimal("500"),
            "transaction_type": "EXPENSE",
            "description": "Grocery Shopping",
        }
    )

    print(result)

    # Copy the ID printed by the tool
    TRANSACTION_ID = input("\nPaste Transaction ID: ").strip()


async def test_list():
    print("\n========== LIST TRANSACTIONS ==========")

    result = await list_transactions.ainvoke(
        {
            "user_id": USER_ID,
        }
    )

    print(result)


async def test_search():
    print("\n========== SEARCH TRANSACTIONS ==========")

    result = await search_transactions.ainvoke(
        {
            "user_id": USER_ID,
            "keyword": "grocery",
        }
    )

    print(result)


async def test_update():
    print("\n========== UPDATE TRANSACTION ==========")

    result = await update_transaction.ainvoke(
        {
            "transaction_id": TRANSACTION_ID,
            "user_id": USER_ID,
            "amount": 800,
            "description": "Monthly Grocery Shopping",
            "transaction_type": "EXPENSE",
        }
    )

    print(result)


async def test_delete():
    print("\n========== DELETE TRANSACTION ==========")

    result = await delete_transaction.ainvoke(
        {
            "transaction_id": TRANSACTION_ID,
            "user_id": USER_ID,
        }
    )

    print(result)


async def main():

    await test_create()

    await test_list()

    await test_search()

    await test_update()

    await test_list()

    await test_delete()

    await test_list()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())