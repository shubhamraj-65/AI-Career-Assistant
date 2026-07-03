
import streamlit as st
import time 
from chatbot.client import llm
from chatbot.config import (
    DEFAULT_MODEL,
    MODELS
)

from chatbot.memory import (
    initialize_memory,
    add_user_message,
    add_assistant_message,
    clear_memory,
    get_messages
)

from utils.constants import (
    APP_TITLE,
    PAGE_TITLE,
    SIDEBAR_TITLE,
    CLEAR_BUTTON,
    SPINNER_TEXT,
    CHAT_INPUT,
    CLEAR_SUCCESS
)

from chatbot.prompts import (
    GENERAL_PROMPT,
    CODING_PROMPT,
    DATA_ANALYST_PROMPT,
    INTERVIEW_PROMPT
)



st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🤖"
)
APP_TITLE = "🤖 AI Career Assistant"

initialize_memory()

# Sidebar for clear history option
with st.sidebar:
    st.title(SIDEBAR_TITLE)

    if st.button(CLEAR_BUTTON, use_container_width=True):
        clear_memory()
        st.success(CLEAR_SUCCESS)

    st.divider()

    st.subheader("🤖 Assistant Mode")

    assistant_mode = st.selectbox(
    "Choose Assistant",
    [
        "General Assistant",
        "Coding Assistant",
        "Data Analyst",
        "Interview Coach"
    ]
)
    
    st.divider()

    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
    )

    max_tokens = st.slider(
        "📄 Max Tokens",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
    )

    top_p = st.slider(
        "🎯 Top P",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.1,
    )
    selected_model = st.selectbox(
    "🧠 Select AI Model",
    list(MODELS.keys()),
    index=0
)

model_name = MODELS[selected_model]

st.caption(f"This chatbot uses {selected_model}")

# Stream response from Groq API
def get_system_prompt():

    if assistant_mode == "Coding Assistant":
        return CODING_PROMPT

    elif assistant_mode == "Data Analyst":
        return DATA_ANALYST_PROMPT

    elif assistant_mode == "Interview Coach":
        return INTERVIEW_PROMPT

    return GENERAL_PROMPT

def stream_response(messages):
    full_response = ""
    message_placeholder = st.empty()

    with llm.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
    ) as response:

        for chunk in response:
            delta_content = chunk.choices[0].delta.content

            if delta_content:
                full_response += delta_content
                message_placeholder.write(full_response)
                time.sleep(0.05)

    return full_response

# Display chat history
for message in get_messages():
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Handle user input
user_input = st.chat_input(CHAT_INPUT)

if user_input:
    add_user_message(user_input)

    st.chat_message("user").write(user_input)

    messages = [
        {
            "role": "system",
            "content": get_system_prompt()
        }
    ]

    messages.extend(get_messages())

    with st.spinner(SPINNER_TEXT):
        answer = stream_response(messages)

    add_assistant_message(answer)