from __future__ import annotations

from app.agents.llm_support import generate_grounded_note
from app.agents.prompts import ORDER_AGENT_PROMPT
from app.graph.state import SmartEatState, add_trace
from app.logging.tracer import log_tool_event
from app.tools.order_tools import create_order_draft
from app.tools.restaurant_tools import get_restaurant_menu


def run_order_agent(state: SmartEatState) -> SmartEatState:
    try:
        selected_restaurant = state["selected_restaurant"]

        if not selected_restaurant:
            state["errors"].append("Order agent skipped because no restaurant was selected.")
            add_trace(
                state,
                agent_name="OrderManagementAgent",
                step="skipped",
                details={"reason": "No selected restaurant"},
            )
            return state

        restaurant_id = selected_restaurant["restaurant_id"]

        log_tool_event(
            "get_restaurant_menu",
            "input",
            {"restaurant_id": restaurant_id},
        )

        menu = get_restaurant_menu(restaurant_id)

        log_tool_event(
            "get_restaurant_menu",
            "output",
            {"restaurant_id": restaurant_id, "menu": menu},
        )

        if not menu:
            state["errors"].append("No available menu items found for selected restaurant.")
            add_trace(
                state,
                agent_name="OrderManagementAgent",
                step="skipped",
                details={"reason": "No available menu items"},
            )
            return state

        chosen_item = menu[0]
        selected_items = [{"menu_id": chosen_item["menu_id"], "quantity": 1}]

        log_tool_event(
            "create_order_draft",
            "input",
            {
                "user_id": state["user_id"],
                "restaurant_id": restaurant_id,
                "items": selected_items,
            },
        )

        draft = create_order_draft(
            user_id=state["user_id"],
            restaurant_id=restaurant_id,
            items=selected_items,
        )

        log_tool_event(
            "create_order_draft",
            "output",
            {"order_draft": draft},
        )

        state["selected_items"] = selected_items
        state["order_total"] = draft["total"]
        state["order_draft"] = draft

        llm_note = generate_grounded_note(
            ORDER_AGENT_PROMPT,
            {
                "selected_restaurant": selected_restaurant,
                "selected_items": selected_items,
                "order_draft": draft,
            },
        )

        add_trace(
            state,
            agent_name="OrderManagementAgent",
            step="order_draft_created",
            details={
                "restaurant_id": restaurant_id,
                "selected_items": selected_items,
                "order_id": draft["order_id"],
                "total": draft["total"],
                "llm_note": llm_note,
            },
        )

    except Exception as exc:
        state["errors"].append(f"Order agent error: {str(exc)}")

        log_tool_event(
            "order_agent",
            "error",
            {"error": str(exc)},
        )

        add_trace(
            state,
            agent_name="OrderManagementAgent",
            step="error",
            details={"error": str(exc)},
        )

    return state