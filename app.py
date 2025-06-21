import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up LLM with token
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
)
model = ChatHuggingFace(llm=llm)

# Initialize chat history in session_state (used internally only)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content='You are a helpful AI assistant')]

# Title and input
st.title("LangChain Chatbot (Memory Enabled)")
user_input = st.text_input("You:", key="user_input")

# Handle submission
if st.button("Send") and user_input:
    # Add user input to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.spinner("AI is thinking..."):
        # Invoke LLM with full history
        response = model.invoke(st.session_state.chat_history)

        # Add AI response to history
        st.session_state.chat_history.append(AIMessage(content=response.content))

        # Display only the last user input and AI response
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI:** {response.content}")
