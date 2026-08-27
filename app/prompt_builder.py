def build_prompt(
    question: str,
    retrieved_documents: list[dict],
) -> str:
    """
    Build the prompt sent to the LLM.
    """

    context = ""

    for index, document in enumerate(
        retrieved_documents,
        start=1,
    ):
        context += (
            f"Document {index}\n"
            f"Source: {document['source_name']}\n\n"
            f"{document['text']}\n\n"
        )

    prompt = f"""
You are an enterprise AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not contained in the context,
say:

"I could not find that information in the provided documents."

Do not make up information.

========================

Context

{context}

========================

Question

{question}

========================

Answer:
"""

    return prompt


if __name__ == "__main__":

    sample_documents = [
        {
            "source_name": "Business Blueprint",
            "text":
                "Revenue Streams include "
                "subscriptions and "
                "marketplace commissions.",
        },
        {
            "source_name": "Flowchart",
            "text":
                "CirQX predicts demand "
                "using sales and weather.",
        },
    ]

    question = (
        "How does CirQX generate revenue?"
    )

    prompt = build_prompt(
        question,
        sample_documents,
    )

    print(prompt)