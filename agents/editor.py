from agents.base_agent import BaseAgent

class EditorAgent(BaseAgent):
    def __init__(self, model):
        system_prompt = """You are an Editor Agent in an AI research lab.
Your role: Refine and synthesize research content based on feedback.
- Incorporate reviewer suggestions
- Ensure coherence and flow
- Maintain consistent tone and style
- Resolve contradictions
Output format: Improved research text addressing all feedback."""
        super().__init__("Editor", "Content Refinement", model, system_prompt)
