import requests
import streamlit as st
import time


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 Enterprise RAG Assistant")

st.caption(
    "Ask questions about your enterprise documents "
    "and get grounded answers with sources."
)


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:
    st.header("Enterprise RAG")

    st.write(
        "This assistant answers questions using "
        "your indexed enterprise documents."
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# -------------------------
# Initialize chat history
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Helper: display sources
# -------------------------

def display_sources(
    sources: list[dict],
) -> None:
    """
    Display retrieved sources in a clean expandable section.
    """

    if not sources:
        return

    with st.expander(
        f"📄 Sources ({len(sources)})"
    ):
        for source_number, source in enumerate(
            sources,
            start=1,
        ):
            source_name = source.get(
                "source_name",
                "Unknown source",
            )

            chunk_index = source.get(
                "chunk_index",
                "N/A",
            )

            retrieval_type = source.get(
                "retrieval_type",
                "retrieved",
            )

            st.markdown(
                f"### Source {source_number}"
            )

            st.markdown(
                f"**File:** {source_name}"
            )

            st.markdown(
                f"**Chunk:** {chunk_index}"
            )

            st.markdown(
                f"**Type:** {retrieval_type}"
            )

            if source.get("score") is not None:
                st.markdown(
                    f"**Similarity Score:** "
                    f"{source['score']:.3f}"
                )

            st.markdown("**Retrieved Text:**")

            st.write(
                source.get(
                    "text",
                    "No source text available.",
                )
            )

            if source_number < len(sources):
                st.divider()


# -------------------------
# Display chat history
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            if "response_time" in message:
                st.caption(
                    f"⏱️ Response Time: "
                    f"{message['response_time']} seconds"
                )

            display_sources(
                message.get(
                    "sources",
                    [],
                )
            )


# -------------------------
# Chat input
# -------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


# -------------------------
# Process new question
# -------------------------

if question:

    user_message = {
        "role": "user",
        "content": question,
    }

    st.session_state.messages.append(
        user_message
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                    },
                    timeout=120,
                )

                response.raise_for_status()

                result = response.json()

                answer = result.get(
                    "answer",
                    (
                        "I could not generate "
                        "an answer."
                    ),
                )

                sources = result.get(
                    "sources",
                    [],
                )

                response_time = round(
                    time.time() - start_time,
                    2,
                )

                st.caption(
                    f"⏱️ Response Time: "
                    f"{response_time} seconds"
                )

                st.markdown(answer)

                display_sources(
                    sources
                )

                assistant_message = {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "response_time": response_time,
                }

                st.session_state.messages.append(
                    assistant_message
                )

            except requests.ConnectionError:

                error_message = (
                    "Could not connect to the FastAPI "
                    "server. Make sure Uvicorn is running."
                )

                st.error(error_message)

            except requests.Timeout:

                error_message = (
                    "The request took too long. "
                    "Please try again."
                )

                st.error(error_message)

            except requests.RequestException as error:

                error_message = (
                    f"API request failed: {error}"
                )

                st.error(error_message)

            except ValueError:

                error_message = (
                    "The API returned an invalid response."
                )

                st.error(error_message)