import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model Settings
GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "openai/gpt-oss-20b"

# Agent Parameters
MAX_ITERATIONS = 2
CONVERGENCE_THRESHOLD = 0.7
TEMPERATURE = 0.9

# Workflow Constants
RESEARCH_SECTIONS = ["introduction", "methodology", "findings", "conclusion"]
QUALITY_METRICS = ["accuracy", "coherence", "completeness"]