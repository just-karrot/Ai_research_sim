from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config.settings import GOOGLE_API_KEY, GROQ_API_KEY, GEMINI_MODEL, GROQ_MODEL, TEMPERATURE

class ModelFactory:
    @staticmethod
    def get_gemini():
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=TEMPERATURE
        )
    
    @staticmethod
    def get_groq():
        return ChatGroq(
            model=GROQ_MODEL,
            groq_api_key=GROQ_API_KEY,
            temperature=TEMPERATURE
        )
    
    @staticmethod
    def get_model(model_type="gemini"):
        return ModelFactory.get_gemini() if model_type == "gemini" else ModelFactory.get_groq()
