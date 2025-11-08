import streamlit as st
import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from workflow.runner import WorkflowRunner
    from config import settings
except ImportError:
    st.error("Module import error. Please ensure all dependencies are installed.")
    st.stop()

st.set_page_config(page_title="AI Research Lab", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'workflow_running' not in st.session_state:
    st.session_state.workflow_running = False
if 'workflow_paused' not in st.session_state:
    st.session_state.workflow_paused = False
if 'process_logs' not in st.session_state:
    st.session_state.process_logs = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None

st.title("🔬 AI Research Lab Simulator")
st.markdown("Multi-agent LLM research pipeline with Gemini and Groq")
st.caption("🔀 Powered by LangGraph StateGraph with iterative refinement")

col1, col2 = st.columns([4, 1])
with col2:
    st.markdown("[💬 Chat with Research](http://localhost:8501)")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Speed Mode
    speed_mode = st.toggle("⚡ Fast Mode", value=True, disabled=st.session_state.workflow_running)
    if speed_mode:
        st.caption("⚡ Using faster models and reduced iterations")
    
    # Model Distribution
    model_dist = st.selectbox(
        "Model Distribution",
        ["Balanced (Gemini+Groq)", "All Gemini", "All Groq"],
        index=0,
        disabled=st.session_state.workflow_running
    )
    
    if model_dist == "All Gemini":
        distribution = {k: "gemini" for k in ["researcher", "reviewer", "editor", "fact_checker", "citation_validator"]}
    elif model_dist == "All Groq":
        distribution = {k: "groq" for k in ["researcher", "reviewer", "editor", "fact_checker", "citation_validator"]}
    else:
        distribution = None
    
    st.divider()
    
    # Workflow Parameters
    st.subheader("🎛️ LangGraph Parameters")
    
    max_iterations = st.slider(
        "Max Iterations",
        min_value=1,
        max_value=10,
        value=1 if speed_mode else settings.MAX_ITERATIONS,
        disabled=st.session_state.workflow_running
    )
    
    convergence_threshold = st.slider(
        "Convergence Threshold",
        min_value=0.5,
        max_value=1.0,
        value=0.6 if speed_mode else settings.CONVERGENCE_THRESHOLD,
        step=0.05,
        disabled=st.session_state.workflow_running
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=settings.TEMPERATURE,
        step=0.1,
        disabled=st.session_state.workflow_running
    )
    
    # Update settings
    settings.MAX_ITERATIONS = max_iterations
    settings.CONVERGENCE_THRESHOLD = convergence_threshold
    settings.TEMPERATURE = temperature
    
    st.divider()
    
    # Graph Nodes
    st.markdown("**Graph Nodes:**")
    agent_status = "🟢 Active" if st.session_state.workflow_running else "⚪ Idle"
    st.markdown(f"Status: {agent_status}")
    st.markdown("- 🔍 Research Node")
    st.markdown("- 📝 Review Node")
    st.markdown("- ✏️ Editor Node")
    st.markdown("- ✅ Fact Check Node")
    st.markdown("- 📚 Citation Node")
    st.markdown("- 🎯 Finalize Node")
    
    st.divider()
    
    # Process Logs
    if st.session_state.process_logs:
        st.subheader("📋 Process Logs")
        log_text = "\n".join(st.session_state.process_logs[-10:])
        st.text_area("Recent Logs", log_text, height=150, disabled=True)
        
        if st.button("📥 Download Logs"):
            log_content = "\n".join(st.session_state.process_logs)
            st.download_button(
                label="Save Logs",
                data=log_content,
                file_name=f"process_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# Main interface
topic = st.text_input(
    "Enter Research Topic:", 
    placeholder="e.g., Impact of AI on Healthcare",
    disabled=st.session_state.workflow_running
)

# Workflow Controls
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
with col1:
    start_btn = st.button(
        "🚀 Start Research", 
        type="primary", 
        use_container_width=True,
        disabled=st.session_state.workflow_running or not topic
    )
with col2:
    stop_btn = st.button(
        "⏹️ Stop", 
        use_container_width=True,
        disabled=not st.session_state.workflow_running
    )
with col3:
    pause_btn = st.button(
        "⏸️ Pause" if not st.session_state.workflow_paused else "▶️ Resume",
        use_container_width=True,
        disabled=not st.session_state.workflow_running
    )
with col4:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# Handle workflow controls
if stop_btn:
    st.session_state.workflow_running = False
    st.session_state.workflow_paused = False
    st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Workflow stopped by user")
    st.warning("⏹️ Workflow stopped")
    st.rerun()

if pause_btn:
    st.session_state.workflow_paused = not st.session_state.workflow_paused
    status = "paused" if st.session_state.workflow_paused else "resumed"
    st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Workflow {status}")
    st.info(f"⏸️ Workflow {status}")
    time.sleep(0.5)

if start_btn and topic:
    st.session_state.workflow_running = True
    st.session_state.process_logs = []
    st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Starting research on: {topic}")
    st.divider()
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 Agent Dialogue", "📄 Results", "🔀 Workflow Graph"])
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Initializing workflow...")
        st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing agents...")
        progress_bar.progress(10)
        
        runner = WorkflowRunner(distribution)
        
        status_text.text("🚀 Running multi-agent research pipeline...")
        st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Pipeline started")
        progress_bar.progress(30)
        
        # Live response container
        live_response = st.empty()
        
        # Dashboard metrics
        with tab1:
            st.subheader("📊 Real-time Metrics")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                iteration_metric = st.empty()
            with metric_col2:
                quality_metric = st.empty()
            with metric_col3:
                agent_metric = st.empty()
            
            st.divider()
            workflow_viz = st.empty()
        
        # Agent dialogue container
        with tab2:
            st.subheader("🤖 Agent Communication")
            dialogue_container = st.container()
        
        # Results container
        with tab3:
            st.subheader("📄 Research Output")
            results_container = st.container()
        
        # Workflow graph
        with tab4:
            st.subheader("🔀 LangGraph Workflow Visualization")
            from workflow.visualizer import get_ascii_diagram, get_mermaid_diagram
            
            st.markdown("### ASCII Diagram")
            st.code(get_ascii_diagram(), language="")
            
            st.divider()
            
            st.markdown("### Mermaid Diagram")
            st.markdown("```mermaid\n" + get_mermaid_diagram() + "\n```")
            
            st.divider()
            
            st.markdown("### Workflow Details")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Nodes (Agents):**
                - 🔍 Research Node
                - 📝 Review Node
                - ✅ Fact Check Node
                - 📚 Citation Node
                - ✏️ Editor Node
                - 🎯 Finalize Node
                """)
            with col2:
                st.markdown("""
                **Edges (Flow):**
                - Sequential: Research → Review → Fact Check → Citation → Editor
                - Conditional: Editor → Decision
                - Loop: Decision → Review (if not converged)
                - Exit: Decision → Finalize (if converged)
                """)
            
            st.info("💡 This is a LangGraph StateGraph with conditional routing and iterative refinement loops.")
        
        # Stream workflow execution
        agent_messages = []
        current_iteration = 0
        current_quality = 0.0
        final_result = None
        
        for i, output in enumerate(runner.stream(topic)):
            if not st.session_state.workflow_running:
                st.warning("Workflow stopped by user")
                break
            
            while st.session_state.workflow_paused:
                time.sleep(0.5)
                if not st.session_state.workflow_running:
                    break
            
            progress = min(30 + (i * 10), 90)
            progress_bar.progress(progress)
            
            for node_name, node_output in output.items():
                st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Node: {node_name}")
                
                # Show live status
                agent_emoji_map = {
                    'research': '🔍',
                    'review': '📝',
                    'fact_check': '✅',
                    'citation': '📚',
                    'editor': '✏️',
                    'finalize': '🎯'
                }
                emoji = agent_emoji_map.get(node_name, '⚙️')
                status_text.text(f"{emoji} Processing: {node_name.upper()}...")
                
                # Store final result
                final_result = node_output
                
                # Update metrics
                if 'iteration' in node_output:
                    current_iteration = node_output['iteration']
                if 'quality_score' in node_output:
                    current_quality = node_output['quality_score']
                
                with tab1:
                    iteration_metric.metric("Current Iteration", current_iteration, delta=None)
                    quality_metric.metric("Quality Score", f"{current_quality:.3f}", delta=None)
                    agent_metric.metric("Messages", len(agent_messages), delta=None)
                    
                    # Workflow visualization with progress
                    stage_map = {
                        'research': '🔍 **Researcher** → 📝 Reviewer → ✅ Fact Checker → 📚 Citation → ✏️ Editor',
                        'review': '🔍 Researcher → 📝 **Reviewer** → ✅ Fact Checker → 📚 Citation → ✏️ Editor',
                        'fact_check': '🔍 Researcher → 📝 Reviewer → ✅ **Fact Checker** → 📚 Citation → ✏️ Editor',
                        'citation': '🔍 Researcher → 📝 Reviewer → ✅ Fact Checker → 📚 **Citation** → ✏️ Editor',
                        'editor': '🔍 Researcher → 📝 Reviewer → ✅ Fact Checker → 📚 Citation → ✏️ **Editor**',
                        'finalize': '✅ **COMPLETE**'
                    }
                    workflow_viz.markdown(f"""
                    **Current Stage:** {node_name.upper()}
                    
                    {stage_map.get(node_name, '⚙️ Processing...')}
                    """)
                    
                    # Show latest response preview
                    if 'agent_messages' in node_output and node_output['agent_messages']:
                        latest_msg = node_output['agent_messages'][-1]
                        live_response.info(f"**Latest from {latest_msg['agent']}:** {latest_msg['content'][:200]}...")
                
                if 'agent_messages' in node_output:
                    agent_messages.extend(node_output['agent_messages'])
                    
                    with tab2:
                        with dialogue_container:
                            for msg in node_output['agent_messages']:
                                agent_name = msg['agent']
                                agent_emoji = {
                                    'researcher': '🔍',
                                    'reviewer': '📝',
                                    'editor': '✏️',
                                    'fact_checker': '✅',
                                    'citation_validator': '📚'
                                }.get(agent_name, '🤖')
                                
                                with st.expander(f"{agent_emoji} {agent_name.upper()} - {datetime.now().strftime('%H:%M:%S')}", expanded=True):
                                    st.markdown(f"**Agent:** {agent_name}")
                                    st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
                                    st.divider()
                                    # Show full content with markdown formatting
                                    st.markdown(msg['content'])
                                    st.caption(f"Length: {len(msg['content'])} chars | Words: {len(msg['content'].split())}")
        
        if st.session_state.workflow_running and final_result:
            status_text.text("Finalizing results...")
            st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Finalizing...")
            progress_bar.progress(95)
            
            # Use result from stream (don't re-run)
            result = final_result
            st.session_state.current_result = result
            
            progress_bar.progress(100)
            status_text.text("✅ Research complete!")
            live_response.success("🎉 All agents have completed their work!")
            st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Research completed successfully")
            st.session_state.workflow_running = False
            
            # Auto-switch to results tab
            st.balloons()
            
            # Display results
            with tab3:
                with results_container:
                    st.divider()
                    
                    # Metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Quality Score", f"{result.get('quality_score', 0):.3f}")
                    with col2:
                        st.metric("Iterations", result.get('iteration', 0))
                    with col3:
                        st.metric("Agent Messages", len(result.get('agent_messages', [])))
                    with col4:
                        word_count = len(result.get('final_document', '').split())
                        st.metric("Word Count", word_count)
                    with col5:
                        duration = len(st.session_state.process_logs)
                        st.metric("Process Steps", duration)
                    
                    st.markdown("---")
                    
                    # Document preview
                    st.markdown("### 📄 Final Document")
                    st.markdown(result.get('final_document', 'No document generated'))
                    
                    st.divider()
                    
                    # Export options
                    st.subheader("📥 Export Options")
                    
                    export_col1, export_col2, export_col3 = st.columns(3)
                    
                    with export_col1:
                        # Download research document
                        research_doc = result.get('final_document', '')
                        st.download_button(
                            label="📄 Download Research",
                            data=research_doc,
                            file_name=f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                        # Store in session for chat
                        if 'research_for_chat' not in st.session_state:
                            st.session_state.research_for_chat = {}
                        st.session_state.research_for_chat[topic] = research_doc
                    
                    with export_col2:
                        # Download full report with metadata
                        full_report = f"""AI RESEARCH LAB REPORT
{'='*50}
Topic: {topic}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Quality Score: {result.get('quality_score', 0):.3f}
Iterations: {result.get('iteration', 0)}
Word Count: {len(result.get('final_document', '').split())}
{'='*50}

{result.get('final_document', '')}

{'='*50}
PROCESS LOGS
{'='*50}
{chr(10).join(st.session_state.process_logs)}
"""
                        st.download_button(
                            label="📊 Download Full Report",
                            data=full_report,
                            file_name=f"full_report_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with export_col3:
                        # Download JSON data
                        json_data = json.dumps({
                            "topic": topic,
                            "timestamp": datetime.now().isoformat(),
                            "quality_score": result.get('quality_score', 0),
                            "iterations": result.get('iteration', 0),
                            "final_document": result.get('final_document', ''),
                            "agent_messages": result.get('agent_messages', []),
                            "process_logs": st.session_state.process_logs
                        }, indent=2)
                        
                        st.download_button(
                            label="💾 Download JSON",
                            data=json_data,
                            file_name=f"research_data_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
            
            st.success("✅ Research workflow completed successfully!")
            
    except Exception as e:
        st.session_state.workflow_running = False
        st.session_state.process_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}")
        st.error(f"Error: {str(e)}")
        st.exception(e)

elif start_btn and not topic:
    st.warning("⚠️ Please enter a research topic")

# Display previous result if available
if st.session_state.current_result and not st.session_state.workflow_running:
    st.divider()
    st.info("💡 Previous research result available. Start a new research or download the existing one.")

# Footer
# Show workflow visualization when not running
if not st.session_state.workflow_running and not st.session_state.current_result:
    st.divider()
    st.subheader("🔀 Workflow Architecture")
    from workflow.visualizer import get_ascii_diagram
    st.code(get_ascii_diagram(), language="")

if not st.session_state.workflow_running:
    st.divider()
    footer_col1, footer_col2, footer_col3 = st.columns([3, 1, 1])
    with footer_col1:
        st.markdown("**Powered by:** LangGraph • LangChain • Gemini • Groq • Streamlit")
    with footer_col2:
        st.markdown(f"**Version:** 1.0.0")
    with footer_col3:
        st.markdown("[💬 Research Chat](http://localhost:8502)")
