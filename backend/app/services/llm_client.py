import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

# Initialize ChatGroq model
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b",
    temperature=0.2
)

def generate_response(prompt: str) -> str:
    """Send prompt to Groq LLM via LangChain and return response text."""
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content
