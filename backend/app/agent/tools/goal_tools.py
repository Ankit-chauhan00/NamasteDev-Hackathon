from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goals import Goal, GoalPriority, GoalStatus
from app.models.user import User
from langchain_core.tools import tool

from app.agent.prompts.goal_prompt import GOAL_ADVICE_PROMPT
from app.core.llm import reasoning_model

# ---------------------------------------------------------------------------
# Tool 1: create_goal
# ---------------------------------------------------------------------------
@tool("create_goal")
async def create_goal(
    db: AsyncSession,
    user_id: UUID,
    title: str,
    target_amount: Decimal,
    priority: GoalPriority = GoalPriority.MEDIUM,
    description: str | None = None,
):
    # Validate amount
    if target_amount <= 0:
        return {
            "success": False,
            "message": "Target amount must be greater than 0."
        }

    # Check if user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Create goal
    goal = Goal(
        title=title,
        description=description,
        target_amount=target_amount,
        current_amount=Decimal("0.00"),
        priority=priority,
        status=GoalStatus.ACTIVE,
        user_id=user_id,
    )

    db.add(goal)
    await db.commit()
    await db.refresh(goal)

    return {
        "success": True,
        "message": "Goal created successfully.",
        "goal": goal,
    }

# ---------------------------------------------------------------------------
# Tool 2: list_goals
# ---------------------------------------------------------------------------
@tool("list_goals")
async def list_goals(
    db: AsyncSession,
    user_id: UUID,
):
    # Check if user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return {
            "success": False,
            "message": "User not found."
        }

    # Fetch all goals
    result = await db.execute(
        select(Goal)
        .where(Goal.user_id == user_id)
        .order_by(Goal.created_at.desc())
    )

    goals = result.scalars().all()

    if not goals:
        return {
            "success": True,
            "message": "No goals found.",
            "goals": []
        }

    return {
        "success": True,
        "message": f"Found {len(goals)} goal(s).",
        "goals": goals,
    }

# ---------------------------------------------------------------------------
# Tool 3: edit_goal
# ---------------------------------------------------------------------------
@tool("edit_goal")
async def edit_goal(

    db: AsyncSession,
    user_id: UUID,
    goal_id: UUID,
    title: str | None = None,
    description: str | None = None,
    target_amount: Decimal | None = None,
    current_amount: Decimal | None = None,
    priority: GoalPriority | None = None,
    status: GoalStatus | None = None,
):
    # Check if goal exists and belongs to the user
    result = await db.execute(
        select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id,
        )
    )
    goal = result.scalar_one_or_none()

    if goal is None:
        return {
            "success": False,
            "message": "Goal not found."
        }

    # Validate amounts
    if target_amount is not None and target_amount <= 0:
        return {
            "success": False,
            "message": "Target amount must be greater than 0."
        }

    if current_amount is not None and current_amount < 0:
        return {
            "success": False,
            "message": "Current amount cannot be negative."
        }

    # Update fields
    if title is not None:
        goal.title = title

    if description is not None:
        goal.description = description

    if target_amount is not None:
        goal.target_amount = target_amount

    if current_amount is not None:
        goal.current_amount = current_amount

    if priority is not None:
        goal.priority = priority

    if status is not None:
        goal.status = status

    await db.commit()
    await db.refresh(goal)

    return {
        "success": True,
        "message": "Goal updated successfully.",
        "goal": goal,
    }

