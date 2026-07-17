from app.db.session import AsyncSessionLocal
from app.agent.tools.analytics_tools import (
    get_account_summary,
    get_income_summary,
    get_expense_summary,
    get_recent_transactions,
)

# Replace with an existing user ID
USER_ID = "12192fd2-1746-4cb0-a02a-223ee473a95a"


async def main():
    async with AsyncSessionLocal() as db:

        print("=" * 15, "ACCOUNT SUMMARY", "=" * 15)
        result = await get_account_summary.ainvoke(
            {
                "db": db,
                "user_id": USER_ID,
            }
        )
        print(result)

        print()

        print("=" * 15, "INCOME SUMMARY", "=" * 15)
        result = await get_income_summary.ainvoke(
            {
                "db": db,
                "user_id": USER_ID,
            }
        )
        print(result)

        print()

        print("=" * 15, "EXPENSE SUMMARY", "=" * 15)
        result = await get_expense_summary.ainvoke(
            {
                "db": db,
                "user_id": USER_ID,
            }
        )
        print(result)

        print()

        print("=" * 15, "RECENT TRANSACTIONS", "=" * 15)
        result = await get_recent_transactions.ainvoke(
            {
                "db": db,
                "user_id": USER_ID,
                "limit": 10,
            }
        )
        print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())