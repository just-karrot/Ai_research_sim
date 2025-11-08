from agents.researcher import ResearcherAgent
from agents.reviewer import ReviewerAgent
from agents.editor import EditorAgent
from agents.fact_checker import FactCheckerAgent
from agents.citation_validator import CitationValidatorAgent
from config.models import ModelFactory

class AgentFactory:
    @staticmethod
    def create_agents(model_distribution=None):
        if model_distribution is None:
            model_distribution = {
                "researcher": "gemini",
                "reviewer": "groq",
                "editor": "gemini",
                "fact_checker": "groq",
                "citation_validator": "gemini"
            }
        
        return {
            "researcher": ResearcherAgent(ModelFactory.get_model(model_distribution["researcher"])),
            "reviewer": ReviewerAgent(ModelFactory.get_model(model_distribution["reviewer"])),
            "editor": EditorAgent(ModelFactory.get_model(model_distribution["editor"])),
            "fact_checker": FactCheckerAgent(ModelFactory.get_model(model_distribution["fact_checker"])),
            "citation_validator": CitationValidatorAgent(ModelFactory.get_model(model_distribution["citation_validator"]))
        }
