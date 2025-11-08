from workflow.graph import create_research_workflow
from agents.agent_factory import AgentFactory

class WorkflowRunner:
    def __init__(self, model_distribution=None):
        self.agents = AgentFactory.create_agents(model_distribution)
        self.workflow = create_research_workflow(self.agents)
    
    def run(self, topic: str):
        initial_state = {
            "topic": topic,
            "research_content": "",
            "review_feedback": "",
            "fact_check_results": "",
            "citation_results": "",
            "quality_score": 0.0,
            "iteration": 0,
            "agent_messages": [],
            "final_document": ""
        }
        
        result = self.workflow.invoke(initial_state)
        return result
    
    def stream(self, topic: str):
        initial_state = {
            "topic": topic,
            "research_content": "",
            "review_feedback": "",
            "fact_check_results": "",
            "citation_results": "",
            "quality_score": 0.0,
            "iteration": 0,
            "agent_messages": [],
            "final_document": ""
        }
        
        for output in self.workflow.stream(initial_state):
            yield output
