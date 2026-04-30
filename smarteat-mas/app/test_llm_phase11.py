from app.llm.ollama_client import run_simple_prompt


def main() -> None:
    system_prompt = (
        "You are a helpful assistant for the SmartEat multi-agent system. "
        "Respond clearly and briefly."
    )

    user_prompt = (
        "A user wants a halal Sri Lankan meal under 2500 in Malabe. "
        "Give a one-sentence assistant response."
    )

    result = run_simple_prompt(system_prompt, user_prompt)

    print("\nLLM RESPONSE:")
    print(result)


if __name__ == "__main__":
    main()