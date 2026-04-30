from __future__ import annotations

from typing import Any, TypedDict

from app.logging.tracer import log_agent_event


class SmartEatState(TypedDict):
    """
    Global shared state passed between SmartEat MAS agents.
    """

    user_id: str
    user_query: str

    constraints: dict[str, Any]
    user_profile: dict[str, Any] | None

    restaurant_candidates: list[dict[str, Any]]
    selected_restaurant: dict[str, Any] | None

    selected_items: list[dict[str, Any]]
    order_total: float | None
    order_draft: dict[str, Any] | None

    notification_message: str | None
    summary_file_path: str | None
    final_response: str | None

    errors: list[str]
    execution_trace: list[dict[str, Any]]


def build_initial_state(user_id: str, user_query: str) -> SmartEatState:
    """
    Build the starting state for a new SmartEat request.

    Args:
        user_id: The user making the request.
        user_query: The natural language request.

    Returns:
        SmartEatState: Initialized state dictionary.
    """
    return SmartEatState(
        user_id=user_id.strip(),
        user_query=user_query.strip(),
        constraints={},
        user_profile=None,
        restaurant_candidates=[],
        selected_restaurant=None,
        selected_items=[],
        order_total=None,
        order_draft=None,
        notification_message=None,
        summary_file_path=None,
        final_response=None,
        errors=[],
        execution_trace=[],
    )


def add_trace(
    state: SmartEatState,
    agent_name: str,
    step: str,
    details: dict[str, Any],
) -> None:
    """
    Append a trace entry to in-memory state and write it to the trace log file.

    Args:
        state: Current global state.
        agent_name: Name of the agent or component.
        step: Short label describing the action.
        details: Extra structured information about the action.
    """
    entry = {
        "agent": agent_name,
        "step": step,
        "details": details,
    }

    state["execution_trace"].append(entry)

    try:
        log_agent_event(agent_name, step, details)
    except Exception:
        # Logging should never break the main workflow
        pass