from __future__ import annotations

from app.agents.llm_support import generate_grounded_note
from app.agents.prompts import NOTIFICATION_AGENT_PROMPT
from app.graph.state import SmartEatState, add_trace
from app.logging.tracer import log_tool_event
from app.tools.notification_tools import save_notification, write_order_summary


def run_notification_agent(state: SmartEatState) -> SmartEatState:
    try:
        if state["order_draft"] is None:
            error_text = " | ".join(state["errors"]) if state["errors"] else "No matching result found."

            message = f"Sorry, SmartEat could not create an order draft. Reason: {error_text}"

            state["notification_message"] = message
            state["final_response"] = message

            add_trace(
                state,
                agent_name="NotificationAgent",
                step="failure_response_created",
                details={"message": message},
            )
            return state

        order = state["order_draft"]
        restaurant = state["selected_restaurant"]
        user_profile = state.get("user_profile") or {}

        llm_note = generate_grounded_note(
            NOTIFICATION_AGENT_PROMPT,
            {
                "user_name": user_profile.get("name", state["user_id"]),
                "restaurant_name": restaurant["name"],
                "order_id": order["order_id"],
                "total": order["total"],
                "currency": order.get("currency", "LKR"),
                "status": order["status"],
                "items": order["items"],
            },
        )

        item_lines = []
        for item in order["items"]:
            item_lines.append(
                f"- {item['item_name']} x{item['quantity']} = {item['line_total']} {order.get('currency', 'LKR')}"
            )

        item_text = "\n".join(item_lines)

        message = (
            f"Hello {user_profile.get('name', state['user_id'])}, your SmartEat order draft "
            f"{order['order_id']} has been created successfully.\n"
            f"Restaurant: {restaurant['name']}\n"
            f"Items:\n{item_text}\n"
            f"Total: {order['total']} {order.get('currency', 'LKR')}\n"
            f"Status: {order['status']}"
        )

        log_tool_event(
            "save_notification",
            "input",
            {"user_id": state["user_id"], "message": message},
        )

        saved_notification = save_notification(state["user_id"], message)

        log_tool_event(
            "save_notification",
            "output",
            {"notification": saved_notification},
        )

        summary_text = (
            f"Order ID: {order['order_id']}\n"
            f"User ID: {state['user_id']}\n"
            f"User Name: {user_profile.get('name', state['user_id'])}\n"
            f"Restaurant: {restaurant['name']}\n"
            f"Total: {order['total']} {order.get('currency', 'LKR')}\n"
            f"Status: {order['status']}\n"
            f"Items: {order['items']}\n"
            f"LLM Note: {llm_note}\n"
            f"Notification Message: {message}\n"
        )

        log_tool_event(
            "write_order_summary",
            "input",
            {"order_id": order["order_id"]},
        )

        summary_file_path = write_order_summary(order["order_id"], summary_text)

        log_tool_event(
            "write_order_summary",
            "output",
            {"summary_file_path": summary_file_path},
        )

        state["notification_message"] = message
        state["summary_file_path"] = summary_file_path
        state["final_response"] = message

        add_trace(
            state,
            agent_name="NotificationAgent",
            step="notification_and_summary_created",
            details={
                "notification_id": saved_notification["notification_id"],
                "summary_file_path": summary_file_path,
                "llm_note": llm_note,
                "message": message,
            },
        )

    except Exception as exc:
        state["errors"].append(f"Notification agent error: {str(exc)}")

        log_tool_event(
            "notification_agent",
            "error",
            {"error": str(exc)},
        )

        add_trace(
            state,
            agent_name="NotificationAgent",
            step="error",
            details={"error": str(exc)},
        )

    return state