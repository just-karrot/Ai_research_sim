import streamlit as st
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agents.agent_factory import AgentFactory

st.set_page_config(page_title="Chat with Agents", layout="wide")

st.title("💬 Chat with Research Agents")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agents' not in st.session_state:
    st.session_state.agents = AgentFactory.create_agents()

# Sidebar - Agent selection
with st.sidebar:
    st.header("🤖 Select Agent")
    
    agent_choice = st.selectbox(
        "Choose an agent to chat with:",
        ["researcher", "reviewer", "editor", "fact_checker", "citation_validator"]
    )
    
    agent_info = {
        "researcher": "🔍 Generates research content",
        "reviewer": "📝 Evaluates quality",
        "editor": "✏️ Refines content",
        "fact_checker": "✅ Validates facts",
        "citation_validator": "📚 Checks citations"
    }
    
    st.info(agent_info[agent_choice])
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask the agent anything..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    agent = st.session_state.agents[agent_choice]
    with st.chat_message("assistant"):
        with st.spinner(f"{agent_choice} is thinking..."):
            response = agent.invoke(prompt)
            st.markdown(response)
    
    # Add assistant message
    st.session_state.chat_history.append({"role": "assistant", "content": response})
