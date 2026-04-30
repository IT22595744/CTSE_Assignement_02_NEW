from __future__ import annotations

from app.agents.llm_support import generate_grounded_note
from app.agents.prompts import RESTAURANT_AGENT_PROMPT
from app.graph.state import SmartEatState, add_trace
from app.logging.tracer import log_tool_event
from app.tools.restaurant_tools import search_restaurants


def run_restaurant_agent(state: SmartEatState) -> SmartEatState:
    try:
        constraints = state["constraints"]

        log_tool_event(
            "search_restaurants",
            "input",
            {"constraints": constraints},
        )

        candidates = search_restaurants(
            location=constraints.get("location"),
            cuisine=constraints.get("cuisine"),
            halal=constraints.get("halal"),
            vegetarian=constraints.get("vegetarian"),
            max_budget=constraints.get("max_budget"),
            only_open=True,
        )

        log_tool_event(
            "search_restaurants",
            "output",
            {"candidate_count": len(candidates), "candidates": candidates},
        )

        state["restaurant_candidates"] = candidates
        state["selected_restaurant"] = candidates[0] if candidates else None

        llm_note = generate_grounded_note(
            RESTAURANT_AGENT_PROMPT,
            {
                "constraints": constraints,
                "candidate_count": len(candidates),
                "candidates": candidates,
                "selected_restaurant": state["selected_restaurant"],
            },
        )

        add_trace(
            state,
            agent_name="RestaurantDiscoveryAgent",
            step="restaurants_searched",
            details={
                "constraints": constraints,
                "candidate_count": len(candidates),
                "selected_restaurant": state["selected_restaurant"],
                "llm_note": llm_note,
            },
        )

        if not candidates:
            state["errors"].append("No matching restaurants found.")

    except Exception as exc:
        state["errors"].append(f"Restaurant agent error: {str(exc)}")

        log_tool_event(
            "search_restaurants",
            "error",
            {"error": str(exc)},
        )

        add_trace(
            state,
            agent_name="RestaurantDiscoveryAgent",
            step="error",
            details={"error": str(exc)},
        )

    return state