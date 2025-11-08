# Speed optimization settings

# Faster model alternatives
FAST_GEMINI_MODEL = "gemini-2.0-flash-exp"  # Already fast
FAST_GROQ_MODEL = "llama-3.1-8b-instant"  # Faster than mixtral

# Reduced complexity
MAX_PROMPT_LENGTH = 500  # Truncate long prompts
MAX_RESPONSE_LENGTH = 1000  # Limit response size

# Parallel processing
ENABLE_PARALLEL = False  # Set True for parallel agent execution (experimental)

# Timeout settings
AGENT_TIMEOUT = 30  # seconds per agent
