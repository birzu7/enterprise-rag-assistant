import os

import requests


OLLAMA_GENERATE_URL = os.getenv(
    "OLLAMA_GENERATE_URL",
    "http://localhost:11434/api/generate",
)

DEFAULT_MODEL = "llama3.2"


def generate_answer(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Send a prompt to Ollama and return
    the generated text.
    """

    if not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty"
        )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
        },
    }

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

    except requests.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is installed and running."
        ) from error

    except requests.Timeout as error:
        raise RuntimeError(
            "Ollama took too long to respond."
        ) from error

    except requests.RequestException as error:
        raise RuntimeError(
            f"Ollama request failed: {error}"
        ) from error

    response_data = response.json()

    answer = response_data.get(
        "response",
        "",
    ).strip()

    if not answer:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return answer


if __name__ == "__main__":
    test_prompt = """
You are a helpful assistant.

Answer this question in simple English:

What is machine learning?
"""

    answer = generate_answer(
        test_prompt
    )

    print("MODEL ANSWER:")
    print(answer)