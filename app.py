1  import streamlit as st
2  from openai import OpenAI

3  client = OpenAI(api_key=st.secrets.OpenAIAPI.openai_api_key)
4  # Obtaining the OpenAI API key from Streamlit Community Cloud's 'Secrets'.

5  # Using st.session_state to store the exchange of messages.
6  if "messages" not in st.session_state:
7      st.session_state["messages"] = [
8          {"role": "system", "content": "You are a trip adviser assistant AI."}
9      ]

10  # Function for interacting with a chatbot.
11  def communicate():
12      messages = st.session_state["messages"]

13      user_message = {"role": "user", "content": st.session_state["user_input"]}
14      st.write("You: " + user_message["content"])  # Added line to display user input
15      messages.append(user_message)

16      response = client.chat.completions.create(model="gpt-3.5-turbo",
17                                              messages=messages
18                                              )
19      bot_message = response.choices[0].message
20      messages.append(bot_message)

21      st.session_state["user_input"] = ""

# User Interface
22  st.title("Trip Adviser AI")
23  st.write("Utilizing the ChatGPT API, this chatbot offers advanced conversational capabilities.")

24  user_input = st.text_input("please enter a message here.", key="user_input", on_change=communicate)

25  if st.session_state["messages"]:
26      messages = st.session_state["messages"]

27      for message in reversed(messages[1:]):
28          speaker = "🙂"
29          if hasattr(message, "role") and message.role == "assistant":
30              speaker = "🤖"

31          if hasattr(message, "content"):
32              st.write(speaker + ": " + message.content)
