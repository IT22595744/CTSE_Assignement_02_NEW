from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from app.database.db import BASE_DIR, get_connection

SUMMARY_DIR = BASE_DIR / "app" / "output" / "order_summaries"
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def save_notification(user_id: str, message: str) -> dict[str, Any]:
    """
    Save a notification message for a user.

    Args:
        user_id: Target user ID.
        message: Notification message.

    Returns:
        dict[str, Any]: Stored notification details.

    Raises:
        ValueError: If user_id or message is empty.
        LookupError: If user does not exist.
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id must not be empty.")

    if not message or not message.strip():
        raise ValueError("message must not be empty.")

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id.strip(),))
        user_row = cursor.fetchone()
        if user_row is None:
            raise LookupError(f"User not found: {user_id}")

        created_at = datetime.now(UTC).isoformat()

        cursor.execute(
            """
            INSERT INTO notifications (user_id, message, is_read, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id.strip(), message.strip(), 0, created_at),
        )
        notification_id = cursor.lastrowid
        connection.commit()

    return {
        "notification_id": notification_id,
        "user_id": user_id.strip(),
        "message": message.strip(),
        "is_read": 0,
        "created_at": created_at,
    }


def write_order_summary(order_id: str, summary: str) -> str:
    """
    Write an order summary to a local text file.

    Args:
        order_id: Order identifier.
        summary: Summary text content.

    Returns:
        str: File path of the saved summary.

    Raises:
        ValueError: If order_id or summary is empty.
    """
    if not order_id or not order_id.strip():
        raise ValueError("order_id must not be empty.")

    if not summary or not summary.strip():
        raise ValueError("summary must not be empty.")

    file_path = SUMMARY_DIR / f"{order_id.strip()}.txt"
    file_path.write_text(summary.strip(), encoding="utf-8")

    return str(file_path)