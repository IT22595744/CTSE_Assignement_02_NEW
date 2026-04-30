from app.agents.notification_agent import run_notification_agent
from app.agents.order_agent import run_order_agent
from app.agents.restaurant_agent import run_restaurant_agent
from app.agents.user_agent import run_user_agent
from app.graph.state import build_initial_state


def main() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    state = run_user_agent(state)
    state = run_restaurant_agent(state)
    state = run_order_agent(state)
    state = run_notification_agent(state)

    print("\nFINAL RESPONSE:")
    print(state["final_response"])

    print("\nSELECTED RESTAURANT:")
    print(state["selected_restaurant"])

    print("\nORDER DRAFT:")
    print(state["order_draft"])

    print("\nERRORS:")
    print(state["errors"])

    print("\nEXECUTION TRACE:")
    for entry in state["execution_trace"]:
        print(entry)


if __name__ == "__main__":
    main()