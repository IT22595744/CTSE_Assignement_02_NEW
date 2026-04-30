from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm() -> ChatOllama:
    """
    Create and return the local Ollama chat model client.

    Returns:
        ChatOllama: Configured Ollama chat model instance.
    """
    model_name = os.getenv("OLLAMA_MODEL", "smollm2:1.7b-instruct-q4_0")

    return ChatOllama(
        model=model_name,
        temperature=0.2,
    )


def run_simple_prompt(system_prompt: str, user_prompt: str) -> str:
    """
    Run a simple local Ollama prompt with system and user messages.

    Args:
        system_prompt: System-level instructions.
        user_prompt: User request content.

    Returns:
        str: Model text response.
    """
    llm = get_llm()

    messages = [
        ("system", system_prompt),
        ("human", user_prompt),
    ]

    response = llm.invoke(messages)

    if hasattr(response, "content"):
        return str(response.content).strip()

    return str(response).strip()