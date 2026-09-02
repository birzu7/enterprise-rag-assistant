DEFAULT_MODEL = "render-test"


def generate_answer(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Temporary stub used to verify that the
    RAG pipeline works on Render without
    calling Ollama.
    """

    if not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty"
        )

    return (
        "Render test successful. "
        "The RAG pipeline reached the LLM step."
    )


if __name__ == "__main__":
    test_prompt = """
You are a helpful assistant.

Answer this question:

What is machine learning?
"""

    answer = generate_answer(
        test_prompt
    )

    print("MODEL ANSWER:")
    print(answer)