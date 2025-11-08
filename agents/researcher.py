from agents.base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    def __init__(self, model):
        system_prompt = """You are a Research Agent in an AI research lab.
Your role: Generate comprehensive research content on given topics.
- Synthesize information from multiple perspectives
- Structure content logically with clear sections
- Provide evidence-based claims
- Maintain academic rigor
Output format: Structured research text with clear sections."""
        super().__init__("Researcher", "Content Generation", model, system_prompt)
