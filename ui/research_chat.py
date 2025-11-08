import streamlit as st
import sys
import os
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agents.agent_factory import AgentFactory
from workflow.runner import WorkflowRunner

st.set_page_config(page_title="Research Chat", layout="wide")

st.title("💬 Interactive Research Chat")
st.markdown("Generate research and chat about it with AI agents")

# Initialize session state
if 'research_document' not in st.session_state:
    st.session_state.research_document = None
if 'research_topic' not in st.session_state:
    st.session_state.research_topic = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agents' not in st.session_state:
    st.session_state.agents = AgentFactory.create_agents()

# Sidebar
with st.sidebar:
    st.header("📚 Research Document")
    
    # Generate new research
    st.subheader("Generate Research")
    topic = st.text_input("Research Topic:", placeholder="e.g., Quantum Computing")
    
    if st.button("🔬 Generate Research", type="primary", use_container_width=True):
        if topic:
            with st.spinner("Generating research..."):
                runner = WorkflowRunner()
                result = runner.run(topic)
                st.session_state.research_document = result.get('final_document', '')
                st.session_state.research_topic = topic
                st.session_state.chat_history = []
                st.success("✅ Research generated!")
                st.rerun()
        else:
            st.warning("Enter a topic first")
    
    st.divider()
    
    # Upload existing research
    st.subheader("Or Upload Research")
    uploaded_file = st.file_uploader("Upload .txt file", type=['txt'])
    if uploaded_file:
        st.session_state.research_document = uploaded_file.read().decode('utf-8')
        st.session_state.research_topic = uploaded_file.name.replace('.txt', '')
        st.session_state.chat_history = []
        st.success("✅ Research loaded!")
    
    st.divider()
    
    # Current research info
    if st.session_state.research_document:
        st.subheader("📄 Current Research")
        st.info(f"**Topic:** {st.session_state.research_topic}")
        st.caption(f"Length: {len(st.session_state.research_document)} chars")
        st.caption(f"Words: {len(st.session_state.research_document.split())}")
        
        with st.expander("View Document"):
            st.text_area("Research", st.session_state.research_document, height=200, disabled=True)
        
        if st.button("🗑️ Clear Research"):
            st.session_state.research_document = None
            st.session_state.research_topic = None
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    
    # Agent selection
    st.subheader("🤖 Select Agent")
    agent_choice = st.selectbox(
        "Chat with:",
        ["researcher", "reviewer", "editor", "fact_checker", "citation_validator"],
        format_func=lambda x: {
            "researcher": "🔍 Researcher",
            "reviewer": "📝 Reviewer", 
            "editor": "✏️ Editor",
            "fact_checker": "✅ Fact Checker",
            "citation_validator": "📚 Citation Validator"
        }[x]
    )

# Main chat interface
if not st.session_state.research_document:
    st.info("👈 Generate or upload a research document to start chatting")
    st.markdown("""
    ### How to use:
    1. **Generate Research**: Enter a topic and click "Generate Research"
    2. **Or Upload**: Upload an existing research document (.txt)
    3. **Chat**: Ask questions about the research
    4. **Switch Agents**: Different agents provide different perspectives
    
    ### Example Questions:
    - "Summarize the key findings"
    - "What are the main arguments?"
    - "Are there any gaps in this research?"
    - "Suggest improvements"
    - "Fact-check the claims"
    """)
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about the research..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response with research context
        agent = st.session_state.agents[agent_choice]
        
        # Create context-aware prompt
        context_prompt = f"""Research Document:
{st.session_state.research_document[:2000]}...

User Question: {prompt}

Provide a helpful response based on the research document above."""
        
        with st.chat_message("assistant"):
            with st.spinner(f"{agent_choice} is analyzing..."):
                response = agent.invoke(context_prompt)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Quick actions
if st.session_state.research_document:
    st.divider()
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Summarize", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user", 
                "content": "Provide a concise summary of this research"
            })
            st.rerun()
    
    with col2:
        if st.button("🔍 Key Points", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "List the key points and findings"
            })
            st.rerun()
    
    with col3:
        if st.button("❓ Questions", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "What questions does this research raise?"
            })
            st.rerun()
    
    with col4:
        if st.button("💡 Improve", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Suggest improvements for this research"
            })
            st.rerun()
