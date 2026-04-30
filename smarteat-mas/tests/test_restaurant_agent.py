from app.agents.restaurant_agent import run_restaurant_agent
from app.agents.user_agent import run_user_agent
from app.graph.state import build_initial_state


def test_restaurant_agent_selects_matching_restaurant() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)

    assert state["selected_restaurant"] is not None
    assert state["selected_restaurant"]["restaurant_id"] == "R001"
    assert len(state["restaurant_candidates"]) >= 1


def test_restaurant_agent_handles_no_match() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me an Arabian vegetarian halal meal under 500 in Kottawa",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)

    assert state["selected_restaurant"] is None
    assert "No matching restaurants found." in state["errors"]