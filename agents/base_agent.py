from typing import Dict, List, Generator
from langchain_core.messages import HumanMessage, SystemMessage

class BaseAgent:
    def __init__(self, name: str, role: str, model, system_prompt: str):
        self.name = name
        self.role = role
        self.model = model
        self.system_prompt = system_prompt
        self.memory: List[Dict] = []
    
    def invoke(self, input_text: str, context: Dict = None) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input_text)
        ]
        response = self.model.invoke(messages)
        
        self.memory.append({
            "input": input_text,
            "output": response.content,
            "context": context
        })
        
        return response.content
    
    def stream(self, input_text: str, context: Dict = None) -> Generator[str, None, None]:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input_text)
        ]
        
        full_response = ""
        for chunk in self.model.stream(messages):
            if hasattr(chunk, 'content'):
                full_response += chunk.content
                yield chunk.content
        
        self.memory.append({
            "input": input_text,
            "output": full_response,
            "context": context
        })
        
        return full_response
    
    def get_memory(self) -> List[Dict]:
        return self.memory
    
    def clear_memory(self):
        self.memory = []
