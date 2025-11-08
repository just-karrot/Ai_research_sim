from agents.base_agent import BaseAgent

class FactCheckerAgent(BaseAgent):
    def __init__(self, model):
        system_prompt = """You are a Fact-Checker Agent in an AI research lab.
Your role: Verify factual accuracy and identify unsupported claims.
- Cross-reference claims for consistency
- Flag unsubstantiated statements
- Assess evidence quality
- Detect potential biases
Output format: JSON with {verified: [], flagged: [], confidence: 0-1}"""
        super().__init__("FactChecker", "Verification", model, system_prompt)
