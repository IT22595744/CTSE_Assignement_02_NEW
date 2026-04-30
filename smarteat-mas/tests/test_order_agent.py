from app.agents.order_agent import run_order_agent
from app.agents.restaurant_agent import run_restaurant_agent
from app.agents.user_agent import run_user_agent
from app.graph.state import build_initial_state


def test_order_agent_creates_order_draft() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)
    state = run_order_agent(state)

    assert state["order_draft"] is not None
    assert state["order_draft"]["status"] == "DRAFT"
    assert state["order_total"] == 1200.0
    assert state["selected_items"] == [{"menu_id": "M001", "quantity": 1}]


def test_order_agent_skips_when_no_restaurant_selected() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me an Arabian vegetarian halal meal under 500 in Kottawa",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)
    state = run_order_agent(state)

    assert state["order_draft"] is None
    assert any("Order agent skipped" in error for error in state["errors"])