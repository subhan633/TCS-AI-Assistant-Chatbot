import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env
load_dotenv()

# Initialize
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "chatbot-index")

# Ensure the API key is loaded (for debugging)
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in environment variables. Check your .env file.")

pc = Pinecone(api_key=PINECONE_API_KEY)

def clear_index():
    index = get_index()
    index.delete(delete_all=True)
    print("✅ Cleared old vectors from Pinecone")

# Get or create index
def get_index():
    if PINECONE_INDEX not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=384,  # embedding size for MiniLM-L6
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(PINECONE_INDEX)
