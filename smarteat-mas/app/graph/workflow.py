from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agents.notification_agent import run_notification_agent
from app.agents.order_agent import run_order_agent
from app.agents.restaurant_agent import run_restaurant_agent
from app.agents.user_agent import run_user_agent
from app.graph.state import SmartEatState


def route_after_restaurant(state: SmartEatState) -> str:
    """
    Decide the next step after restaurant search.

    Args:
        state: Current SmartEat global state.

    Returns:
        str: Next node name.
    """
    if state.get("selected_restaurant") is not None:
        return "order_agent"

    return "notification_agent"


def build_workflow():
    """
    Build and compile the SmartEat LangGraph workflow.

    Returns:
        Compiled LangGraph application.
    """
    workflow = StateGraph(SmartEatState)

    workflow.add_node("user_agent", run_user_agent)
    workflow.add_node("restaurant_agent", run_restaurant_agent)
    workflow.add_node("order_agent", run_order_agent)
    workflow.add_node("notification_agent", run_notification_agent)

    workflow.add_edge(START, "user_agent")
    workflow.add_edge("user_agent", "restaurant_agent")

    workflow.add_conditional_edges(
        "restaurant_agent",
        route_after_restaurant,
        {
            "order_agent": "order_agent",
            "notification_agent": "notification_agent",
        },
    )

    workflow.add_edge("order_agent", "notification_agent")
    workflow.add_edge("notification_agent", END)

    return workflow.compile()