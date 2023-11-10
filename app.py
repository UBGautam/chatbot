
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.OpenAIAPI.openai_api_key)
# Obtaining the OpenAI API key from Streamlit Community Cloud's 'Secrets'.

# Using st.session_state to store the exchange of messages.
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a trip adviser assistant AI."}
        ]

# Function for interacting with a chatbot.
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages
    )
    bot_message = response.choices[0].message
    messages.append(bot_message)
    
    st.session_state["user_input"] = ""


# User Interface
st.title("Trip Adviser AI")
st.write("Utilizing the ChatGPT API, this chatbot offers advanced conversational capabilities.")

user_input = st.text_input("please enter a message here.", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]): 
        speaker = "🙂"
        if message.role == "assistant":
            speaker="🤖"

        st.write(speaker + ": " + message.content)
