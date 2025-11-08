from typing import TypedDict, List, Dict, Annotated
import operator

class ResearchState(TypedDict):
    topic: str
    research_content: str
    review_feedback: str
    fact_check_results: str
    citation_results: str
    quality_score: float
    iteration: int
    agent_messages: Annotated[List[Dict], operator.add]
    final_document: str
