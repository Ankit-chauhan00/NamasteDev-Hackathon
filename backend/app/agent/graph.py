from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode
from typing import Annotated, TypedDict
import json

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from app.core.llm import reasoning_model,extraction_model
from app.agent.prompts.prompt import SYSTEM_PROMPT
from app.agent.tools.combine_all_tools import ALL_TOOLS


# bind tools with llm
model_with_tools = reasoning_model.bind_tools(ALL_TOOLS)


# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: str



# -----------------------------
# Assistant Node
# -----------------------------
async def call_model(state: AgentState):

    messages = state["messages"]

    # Inject system prompt only once
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    try:
        response = await model_with_tools.ainvoke(messages)

    except Exception:
        fallback = extraction_model.bind_tools(ALL_TOOLS)
        response = await fallback.ainvoke(messages)
    return {"messages": [response]}


# -----------------------------
# Conditional Edge
# -----------------------------
def should_continue(state: AgentState):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return END



# -----------------------------
# Tool Node
# -----------------------------
tool_node = ToolNode(ALL_TOOLS)


# -----------------------------
# Graph
# -----------------------------
workflow = StateGraph(AgentState)

workflow.add_node("assistant", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "assistant")

workflow.add_conditional_edges("assistant", should_continue, {"tools": "tools", END: END})

workflow.add_edge("tools", "assistant")

finance_agent = workflow.compile()


async def run_agent(
    user_message: str,
    user_id: str,
    history: list[tuple[str, str]] | None = None,
):
    """
        Runs a single conversation turn through the LangGraph agent.

    Args:
        user_message: The latest message from the user.
        history: Optional chat history as (role, content) tuples.

    Returns:
        A dictionary containing:
        - reply
        - tool_calls
        - tool_results
        - execution_trace
    """

    messages = []
    for role, content in history or []:
        messages.append(
            HumanMessage(content=content)
            if role == "user"
            else AIMessage(content=content)
        )
    messages.append(HumanMessage(content=user_message))

    result = await finance_agent.ainvoke({"messages": messages, "user_id": user_id},config={"recursion_limit": 20},)
    final_message = result["messages"][-1]
    reply = final_message.content

    if isinstance(reply, list):
        parts = []

        for block in reply:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            elif hasattr(block, "text"):
                parts.append(block.text)
            else:
                parts.append(str(block))

        reply = " ".join(parts)

    elif not isinstance(reply, str):
        reply = str(reply)
    

    tool_calls = []
    tool_results = []
    form_data = None

    for message in result["messages"]:

        # AI requested a tool
        if getattr(message, "tool_calls", None):
            for tool in message.tool_calls:
                tool_calls.append(
                    {
                        "name": tool["name"],
                        "args": tool["args"],
                    }
                )

        # Tool execution result
        if getattr(message, "type", None) == "tool":

            output = message.content

            # Convert json String -> Python dict
            try:
                output = json.loads(output)
            except Exception:
                pass

            # Save form_data if present
            if isinstance(output, dict) and "form_data" in output:
                form_data = output["form_data"]

            tool_results.append(
            {
                "tool_name": getattr(message, "name", ""),
                "output": output,
            }
            )

    execution_trace = ["Received user message"]

    for tool in tool_calls:
        execution_trace.append(f"Selected tool: {tool['name']}")

    for tool in tool_results:
        execution_trace.append(f"Executed tool: {tool['tool_name']}")

    execution_trace.append("Generated final response")

    return {
        "reply": reply,
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "execution_trace": execution_trace,
        "form_data": form_data
    }

