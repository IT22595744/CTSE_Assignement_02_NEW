from __future__ import annotations

import re

from app.agents.llm_support import generate_grounded_note
from app.agents.prompts import USER_AGENT_PROMPT
from app.graph.state import SmartEatState, add_trace
from app.logging.tracer import log_tool_event
from app.tools.user_tools import get_user_profile


def extract_constraints_from_query(user_query: str) -> dict:
    query_lower = user_query.lower()

    budget_match = re.search(r"under\s+(\d+)", query_lower)
    budget = float(budget_match.group(1)) if budget_match else None

    cuisine = None
    for value in ["sri lankan", "indian", "chinese", "arabian"]:
        if value in query_lower:
            cuisine = value.title() if value != "sri lankan" else "Sri Lankan"
            break

    location = None
    for value in ["malabe", "kottawa", "nugegoda"]:
        if value in query_lower:
            location = value.title()
            break

    vegetarian = "vegetarian" in query_lower or "veg" in query_lower

    return {
        "max_budget": budget,
        "cuisine": cuisine,
        "location": location,
        "halal": True if "halal" in query_lower else None,
        "vegetarian": True if vegetarian else None,
    }


def run_user_agent(state: SmartEatState) -> SmartEatState:
    try:
        log_tool_event(
            "get_user_profile",
            "input",
            {"user_id": state["user_id"]},
        )

        profile = get_user_profile(state["user_id"])

        log_tool_event(
            "get_user_profile",
            "output",
            {"user_profile": profile},
        )

        extracted = extract_constraints_from_query(state["user_query"])

        merged_constraints = {
            "max_budget": extracted["max_budget"] if extracted["max_budget"] is not None else profile.get("budget_preference"),
            "cuisine": extracted["cuisine"] if extracted["cuisine"] else profile.get("preferred_cuisine"),
            "location": extracted["location"] if extracted["location"] else profile.get("default_location"),
            "halal": extracted["halal"] if extracted["halal"] is not None else (profile.get("dietary_preference") == "halal"),
            "vegetarian": extracted["vegetarian"] if extracted["vegetarian"] is not None else (profile.get("dietary_preference") == "vegetarian"),
        }

        state["user_profile"] = profile
        state["constraints"] = merged_constraints

        llm_note = generate_grounded_note(
            USER_AGENT_PROMPT,
            {
                "user_profile": profile,
                "extracted_constraints": extracted,
                "merged_constraints": merged_constraints,
            },
        )

        add_trace(
            state,
            agent_name="UserPreferenceAgent",
            step="profile_loaded_and_constraints_extracted",
            details={
                "user_profile": profile,
                "constraints": merged_constraints,
                "llm_note": llm_note,
            },
        )

    except Exception as exc:
        state["errors"].append(f"User agent error: {str(exc)}")

        log_tool_event(
            "get_user_profile",
            "error",
            {"error": str(exc)},
        )

        add_trace(
            state,
            agent_name="UserPreferenceAgent",
            step="error",
            details={"error": str(exc)},
        )

    return state