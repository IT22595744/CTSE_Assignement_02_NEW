from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from app.database.db import BASE_DIR

load_dotenv()

env_log_path = os.getenv("LOG_PATH", "logs/trace.jsonl")

if Path(env_log_path).is_absolute():
    LOG_PATH = Path(env_log_path)
else:
    LOG_PATH = (BASE_DIR / env_log_path).resolve()

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_log_path() -> str:
    """
    Return the absolute path of the trace log file.
    """
    return str(LOG_PATH)


def reset_trace_file() -> None:
    """
    Clear the trace log file for a fresh run.
    """
    LOG_PATH.write_text("", encoding="utf-8")


def append_log(record: dict[str, Any]) -> None:
    """
    Append a structured JSON log record to the trace file.

    Args:
        record: Structured log record.
    """
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        **record,
    }

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def log_agent_event(agent_name: str, step: str, details: dict[str, Any]) -> None:
    """
    Log an agent-level trace event.

    Args:
        agent_name: Name of the agent.
        step: Step label.
        details: Structured details.
    """
    append_log(
        {
            "type": "agent_event",
            "agent": agent_name,
            "step": step,
            "details": details,
        }
    )


def log_tool_event(tool_name: str, stage: str, details: dict[str, Any]) -> None:
    """
    Log a tool call event.

    Args:
        tool_name: Name of the tool.
        stage: Stage such as input, output, or error.
        details: Structured details.
    """
    append_log(
        {
            "type": "tool_event",
            "tool": tool_name,
            "stage": stage,
            "details": details,
        }
    )