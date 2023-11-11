import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.OpenAIAPI.openai_api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a trip adviser assistant AI."}
    ]


def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=messages
                                              )
    bot_message = response.choices[0]
    messages.append({"role": "assistant", "content": bot_message.content})

    st.session_state["user_input"] = ""


st.title("Trip Adviser AI")
st.write("Utilizing the ChatGPT API, this chatbot offers advanced conversational capabilities.")

user_input = st.text_input("please enter a message here.", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):
        speaker = "🙂"
        if hasattr(message, "role") and message.role == "assistant":
            speaker = "🤖"

        # Extract the message content from the ChatCompletionMessage
        if isinstance(message, dict):
            if message["role"] == "assistant":
                speaker = "🤖"
                message_content = message["content"]
            else:
                speaker = "🙂"
                message_content = message["content"]
        else:
            message_content = message

        st.write(speaker + ": " + message_content)
