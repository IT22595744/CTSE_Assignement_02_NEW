from app.graph.state import build_initial_state
from app.graph.workflow import build_workflow


def main() -> None:
    app_graph = build_workflow()

    initial_state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    final_state = app_graph.invoke(initial_state)

    print("\nFINAL RESPONSE:")
    print(final_state["final_response"])

    print("\nSELECTED RESTAURANT:")
    print(final_state["selected_restaurant"])

    print("\nORDER DRAFT:")
    print(final_state["order_draft"])

    print("\nERRORS:")
    print(final_state["errors"])

    print("\nEXECUTION TRACE:")
    for entry in final_state["execution_trace"]:
        print(entry)


if __name__ == "__main__":
    main()