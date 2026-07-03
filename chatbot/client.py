from groq import Groq
from chatbot.config import GROQ_API_KEY

llm = Groq(api_key=GROQ_API_KEY)