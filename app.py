import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os
from dotenv import dotenv_values

secrets = dotenv_values('.env')
# App title
st.set_page_config(page_title="👽👽 ArchieChat")

# Hugging Face Credentials
with st.sidebar:
    st.title('👽👽 ArchieChat')
    if ('EMAIL' in secrets) and ('PASSWORD' in secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = secrets['EMAIL']
        hf_pass = secrets['PASSWORD']
    else:
        hf_email = st.text_input('Enter E-mail:', type='default')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Sign in successful. close window!', icon='👉')
    st.markdown('You can sign up on [Hugging Face](https://huggingface.co/join)')

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "You are a helpful assistant."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.chat(prompt)

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)