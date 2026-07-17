# import asyncio
# import json
# from uuid import uuid4

# from app.agent.graph import run_agent


# async def main():
#     # Dummy user id
#     user_id = "12192fd2-1746-4cb0-a02a-223ee473a95a"

#     print("=" * 60)
#     print("TEST 1 : General Greeting")
#     print("=" * 60)

#     result = await run_agent(
#         user_message="Hello!",
#         user_id=user_id,
#     )

#     print(json.dumps(result, indent=4))

#     print("\n" + "=" * 60)
#     print("TEST 2 : Create Account")
#     print("=" * 60)

#     result = await run_agent(
#         user_message="Create a savings account with balance 10000.",
#         user_id=user_id,
#     )

#     print(json.dumps(result, indent=4))

#     print("\n" + "=" * 60)
#     print("TEST 3 : List Accounts")
#     print("=" * 60)

#     result = await run_agent(
#         user_message="Show all my accounts.",
#         user_id=user_id,
#     )

#     print(json.dumps(result, indent=4))

#     print("\n" + "=" * 60)
#     print("TEST 4 : Create Expense")
#     print("=" * 60)

#     result = await run_agent(
#         user_message="I spent ₹500 on lunch from my savings account.",
#         user_id=user_id,
#     )

#     print(json.dumps(result, indent=4))

#     print("\n" + "=" * 60)
#     print("TEST 5 : Account Summary")
#     print("=" * 60)

#     result = await run_agent(
#         user_message="Give me my financial summary.",
#         user_id=user_id,
#     )

#     print(json.dumps(result, indent=4))


# if __name__ == "__main__":
#     asyncio.run(main())

from app.agent.graph import run_agent

import asyncio
import json


async def main():
    print("=" * 60)
    print("TEST 6 : Create Goal")
    print("=" * 60)

    result = await run_agent(
        user_message="Create a savings goal named Laptop Fund with a target amount of ₹100000.",
        user_id="12192fd2-1746-4cb0-a02a-223ee473a95a",
    )

    print(json.dumps(result, indent=4, default=str))

if __name__ == "__main__":
    asyncio.run(main())