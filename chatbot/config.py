import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("groq_api_key")
DEFAULT_MODEL = "openai/gpt-oss-20b"

MODELS = {
    "GPT OSS 20B": "openai/gpt-oss-20b",
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Gemma 2 9B": "gemma2-9b-it"
}