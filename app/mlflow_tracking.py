import mlflow


MLFLOW_TRACKING_URI = "http://host.docker.internal:5000"
EXPERIMENT_NAME = "enterprise-rag"

#mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
#mlflow.set_experiment(EXPERIMENT_NAME)


def track_rag_run(
    question,
    answer,
    sources,
    response_time,
    top_k,
):
    """
    Log one RAG request to MLflow.
    """

    # Get similarity scores only from sources
    # that actually contain a score.
    retrieval_scores = [
        source["score"]
        for source in sources
        if source.get("score") is not None
    ]

    # Count semantic matches.
    semantic_matches = sum(
        1
        for source in sources
        if source.get("retrieval_type") == "semantic_match"
    )

    # Count neighbor chunks added by context expansion.
    neighbor_chunks = sum(
        1
        for source in sources
        if source.get("retrieval_type") == "neighbor"
    )

    # Calculate total context size.
    context_characters = sum(
        len(source.get("text", ""))
        for source in sources
    )

    with mlflow.start_run():

        # -------------------------
        # Parameters
        # -------------------------

        mlflow.log_param(
            "llm_model",
            "llama3.2",
        )

        mlflow.log_param(
            "embedding_model",
            "all-MiniLM-L6-v2",
        )

        mlflow.log_param(
            "top_k",
            top_k,
        )

        mlflow.log_param(
            "number_of_sources",
            len(sources),
        )

        mlflow.log_param(
            "semantic_matches",
            semantic_matches,
        )

        mlflow.log_param(
            "neighbor_chunks",
            neighbor_chunks,
        )

        # -------------------------
        # Metrics
        # -------------------------

        mlflow.log_metric(
            "response_time_seconds",
            response_time,
        )

        mlflow.log_metric(
            "context_characters",
            context_characters,
        )

        if retrieval_scores:

            mlflow.log_metric(
                "best_retrieval_score",
                max(retrieval_scores),
            )

            mlflow.log_metric(
                "average_retrieval_score",
                sum(retrieval_scores)
                / len(retrieval_scores),
            )

        # -------------------------
        # Tags
        # -------------------------

        mlflow.set_tag(
            "question",
            question,
        )

        # -------------------------
        # Artifacts
        # -------------------------

        mlflow.log_text(
            answer,
            "answer.txt",
        )