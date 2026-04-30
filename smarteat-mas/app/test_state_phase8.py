from app.graph.state import build_initial_state, add_trace


def main() -> None:
    state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe"
    )

    add_trace(
        state,
        agent_name="System",
        step="state_initialized",
        details={
            "user_id": state["user_id"],
            "query": state["user_query"],
        },
    )

    print(state)


if __name__ == "__main__":
    main()