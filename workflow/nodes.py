from workflow.state import ResearchState
from tools.tool_manager import ToolManager
import json

# Initialize with Gemini for knowledge retrieval
tool_manager = ToolManager(retrieval_model="gemini")

def research_node(state: ResearchState, agents) -> ResearchState:
    researcher = agents["researcher"]
    prompt = f"Research topic: {state['topic']}\n\nGenerate concise research content with key findings."
    content = researcher.invoke(prompt)
    
    return {
        "research_content": content,
        "agent_messages": [{"agent": "researcher", "content": content}]
    }

def review_node(state: ResearchState, agents) -> ResearchState:
    reviewer = agents["reviewer"]
    quality_metrics = tool_manager.evaluate_quality(
        state['research_content'], 
        state.get('fact_check_results', ''),
        ['introduction', 'findings', 'conclusion']
    )
    
    prompt = f"Review: {state['research_content'][:500]}\n\nProvide brief feedback and score (0-1)."
    feedback = reviewer.invoke(prompt)
    
    try:
        feedback_json = json.loads(feedback)
        score = feedback_json.get("score", quality_metrics['overall'])
    except:
        score = quality_metrics['overall']
    
    return {
        "review_feedback": feedback,
        "quality_score": score,
        "agent_messages": [{"agent": "reviewer", "content": feedback}]
    }

def fact_check_node(state: ResearchState, agents) -> ResearchState:
    fact_checker = agents["fact_checker"]
    fact_validation = tool_manager.validate_facts(state['research_content'])
    
    prompt = f"Fact-check: {state['research_content'][:400]}\n\nQuick validation."
    results = fact_checker.invoke(prompt)
    
    return {
        "fact_check_results": results,
        "agent_messages": [{"agent": "fact_checker", "content": results}]
    }

def citation_node(state: ResearchState, agents) -> ResearchState:
    citation_validator = agents["citation_validator"]
    citation_analysis = tool_manager.validate_citations(state['research_content'])
    
    prompt = f"Check citations: {state['research_content'][:400]}\n\nBrief validation."
    results = citation_validator.invoke(prompt)
    
    return {
        "citation_results": results,
        "agent_messages": [{"agent": "citation_validator", "content": results}]
    }

def editor_node(state: ResearchState, agents) -> ResearchState:
    editor = agents["editor"]
    prompt = f"""Refine: {state['research_content'][:500]}

Feedback: {state['review_feedback'][:200]}

Produce improved version."""
    
    refined = editor.invoke(prompt)
    
    return {
        "research_content": refined,
        "iteration": state["iteration"] + 1,
        "agent_messages": [{"agent": "editor", "content": refined}]
    }

def finalize_node(state: ResearchState, agents) -> ResearchState:
    return {
        "final_document": state["research_content"]
    }
