from langgraph.graph import StateGraph, END
from workflow.state import ResearchState
from workflow.nodes import (
    research_node, review_node, fact_check_node, 
    citation_node, editor_node, finalize_node
)
from config.settings import MAX_ITERATIONS, CONVERGENCE_THRESHOLD

def should_continue(state: ResearchState) -> str:
    if state["iteration"] >= MAX_ITERATIONS:
        return "finalize"
    if state.get("quality_score", 0) >= CONVERGENCE_THRESHOLD:
        return "finalize"
    return "continue"

def create_research_workflow(agents):
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("research", lambda s: research_node(s, agents))
    workflow.add_node("review", lambda s: review_node(s, agents))
    workflow.add_node("fact_check", lambda s: fact_check_node(s, agents))
    workflow.add_node("citation", lambda s: citation_node(s, agents))
    workflow.add_node("editor", lambda s: editor_node(s, agents))
    workflow.add_node("finalize", lambda s: finalize_node(s, agents))
    
    # Set entry point
    workflow.set_entry_point("research")
    
    # Add edges
    workflow.add_edge("research", "review")
    workflow.add_edge("review", "fact_check")
    workflow.add_edge("fact_check", "citation")
    workflow.add_edge("citation", "editor")
    
    # Conditional routing
    workflow.add_conditional_edges(
        "editor",
        should_continue,
        {
            "continue": "review",
            "finalize": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    return workflow.compile()
