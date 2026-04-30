from __future__ import annotations

import json
from typing import Any

from app.llm.ollama_client import run_simple_prompt


def generate_grounded_note(system_prompt: str, payload: dict[str, Any]) -> str:
    """
    Generate a short grounded note from local structured data.

    Args:
        system_prompt: Agent system instructions.
        payload: Structured local data for the model.

    Returns:
        str: Model-generated grounded note.
    """
    user_prompt = (
        "Use only this local structured data.\n"
        "Do not invent anything.\n"
        "Return a short response.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )

    try:
        return run_simple_prompt(system_prompt, user_prompt)
    except Exception:
        return "LLM note generation skipped due to local model issue."