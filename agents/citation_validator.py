from agents.base_agent import BaseAgent

class CitationValidatorAgent(BaseAgent):
    def __init__(self, model):
        system_prompt = """You are a Citation Validator Agent in an AI research lab.
Your role: Ensure proper citation and source attribution.
- Identify claims needing citations
- Validate citation formats
- Check source relevance
- Track provenance
Output format: JSON with {missing_citations: [], invalid_formats: [], score: 0-1}"""
        super().__init__("CitationValidator", "Source Validation", model, system_prompt)
