import streamlit as st
import random
import time
from openai import OpenAI

st.set_page_config(
    page_title="Chatbot", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items=None)

st.title("Chatbot like ChatGPT")

client = OpenAI(api_key = st.secrets["OPEN_API_KEY"])

# Instantiate a model
if "openai_model" not in st.session_state:
    st.session_state["model"] = "gpt-3.5-turbo"
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty() #empty container
        full_response = ""
        
        
        # Simulate stream of response with milliseconds delay
        for response in OpenAI.chat.completions.create(
            # 3 parameters are passed to the chat completion function
            model = st.state_session["model"],
            messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.message],
            streaming = True
        ):
            #creating streaming response
            time.sleep(0.05)
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown = "▌"
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})