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
                                               messages=messages)
    bot_message = response.choices[0]

    # Check for 'text' attribute instead of 'content'
    if hasattr(bot_message, 'text'):
        message_content = bot_message.text
    else:
        # Handle the case where neither 'content' nor 'text' exists
        raise AttributeError("Unable to extract message content from bot response")

    # Format the bot's response with the desired emoji
    formatted_response = "🤖: " + message_content

    messages.append({"role": "assistant", "content": formatted_response})

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

        if isinstance(message, dict):
            if message["role"] == "user":
                st.write(speaker + ": " + message["content"])
            else:
                st.write(speaker + ": " + message.content)
        else:
            st.write(message)
