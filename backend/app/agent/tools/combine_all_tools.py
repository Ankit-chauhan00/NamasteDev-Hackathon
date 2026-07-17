from app.agent.tools.account_tools import (
    create_account,
    list_user_account,
    update_account,
    delete_account,
)

from app.agent.tools.transaction_tools import (
    create_transaction,
    list_transactions,
    search_transactions,
    update_transaction,
    delete_transaction,
)

from app.agent.tools.goal_tools import (
    create_goal,
    list_goals,
    edit_goal,
)

from app.agent.tools.analytics_tools import (
    get_account_summary,
    get_income_summary,
    get_expense_summary,
    get_recent_transactions,
)


ALL_TOOLS = [
    create_account,
    list_user_account,
    update_account,
    delete_account,

    create_transaction,
    list_transactions,
    search_transactions,
    update_transaction,
    delete_transaction,

    create_goal,
    list_goals,
    edit_goal,

    get_account_summary,
    get_income_summary,
    get_expense_summary,
    get_recent_transactions,

]