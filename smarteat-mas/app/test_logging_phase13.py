from app.graph.state import build_initial_state
from app.graph.workflow import build_workflow
from app.logging.tracer import get_log_path, reset_trace_file


def main() -> None:
    reset_trace_file()

    app_graph = build_workflow()

    initial_state = build_initial_state(
        user_id="U001",
        user_query="Find me a halal Sri Lankan meal under 2500 in Malabe",
    )

    final_state = app_graph.invoke(initial_state)

    print("\nFINAL RESPONSE:")
    print(final_state["final_response"])

    print("\nTRACE LOG PATH:")
    print(get_log_path())

    print("\nTRACE ENTRY COUNT:")
    print(len(final_state["execution_trace"]))


if __name__ == "__main__":
    main()