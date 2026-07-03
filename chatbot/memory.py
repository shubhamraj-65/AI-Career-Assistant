import streamlit as st


def initialize_memory():
    """Initialize chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_user_message(message):
    """Add user message."""
    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )


def add_assistant_message(message):
    """Add assistant message."""
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message
        }
    )


def clear_memory():
    """Clear chat history."""
    st.session_state.messages = []


def get_messages():
    """Return chat history."""
    return st.session_state.messages