from pathlib import Path

from app.agents.notification_agent import run_notification_agent
from app.agents.order_agent import run_order_agent
from app.agents.restaurant_agent import run_restaurant_agent
from app.agents.user_agent import run_user_agent
from app.graph.state import build_initial_state


def test_notification_agent_creates_final_response_and_summary() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)
    state = run_order_agent(state)
    state = run_notification_agent(state)

    assert state["final_response"] is not None
    assert "Hello Ahamed" in state["final_response"]
    assert "Malabe Kottu House" in state["final_response"]
    assert state["summary_file_path"] is not None
    assert Path(state["summary_file_path"]).exists()


def test_notification_agent_handles_failure_case() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me an Arabian vegetarian halal meal under 500 in Kottawa",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)
    state = run_notification_agent(state)

    assert state["order_draft"] is None
    assert state["final_response"] is not None
    assert state["final_response"].startswith("Sorry, SmartEat could not create an order draft.")