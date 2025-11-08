from config.models import ModelFactory
from langchain_core.messages import HumanMessage, SystemMessage

class KnowledgeRetriever:
    def __init__(self, model_type="gemini"):
        self.model = ModelFactory.get_model(model_type)
    
    def retrieve(self, topic: str) -> str:
        messages = [
            SystemMessage(content="You are a knowledge retrieval system. Provide factual, comprehensive information on the given topic."),
            HumanMessage(content=f"Provide key facts and context about: {topic}")
        ]
        response = self.model.invoke(messages)
        return response.content
