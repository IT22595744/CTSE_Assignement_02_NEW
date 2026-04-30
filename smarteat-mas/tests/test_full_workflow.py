from app.graph.state import build_initial_state
from app.graph.workflow import build_workflow


def test_full_workflow_success() -> None:
    app_graph = build_workflow()

    initial_state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    final_state = app_graph.invoke(initial_state)

    assert final_state["errors"] == []
    assert final_state["selected_restaurant"] is not None
    assert final_state["order_draft"] is not None
    assert "Hello Ahamed" in final_state["final_response"]
    assert len(final_state["execution_trace"]) == 4


def test_full_workflow_no_match() -> None:
    app_graph = build_workflow()

    initial_state = build_initial_state(
        user_id="U001",
        user_query="Find me an Arabian vegetarian halal meal under 500 in Kottawa",
    )

    final_state = app_graph.invoke(initial_state)

    assert final_state["selected_restaurant"] is None
    assert final_state["order_draft"] is None
    assert final_state["final_response"].startswith("Sorry, SmartEat could not create an order draft.")
    assert "No matching restaurants found." in final_state["errors"]