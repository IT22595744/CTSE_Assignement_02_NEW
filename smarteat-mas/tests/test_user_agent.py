from app.agents.user_agent import run_user_agent
from app.graph.state import build_initial_state


def test_user_agent_loads_profile_and_constraints() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    state = run_user_agent(state)

    assert state["user_profile"] is not None
    assert state["user_profile"]["name"] == "Ahamed"
    assert state["constraints"]["location"] == "Malabe"
    assert state["constraints"]["cuisine"] == "Sri Lankan"
    assert state["constraints"]["halal"] is True
    assert state["constraints"]["max_budget"] == 2500.0
    assert state["errors"] == []


def test_user_agent_handles_unknown_user() -> None:
    state = build_initial_state(
        user_id="U999",
        user_query="Find me a meal",
    )

    state = run_user_agent(state)

    assert state["user_profile"] is None
    assert len(state["errors"]) >= 1
    assert "User agent error" in state["errors"][0]