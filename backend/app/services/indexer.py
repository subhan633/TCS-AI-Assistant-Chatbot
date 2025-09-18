import os
import json
from app.services.embeddings import get_embedding
from app.services.pinecone_client import get_index

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data", "kb")

def index_kb():
    index = get_index()
    documents = []

    # Load all KB JSON files
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".json"):
            with open(os.path.join(DATA_DIR, file_name), "r", encoding="utf-8") as f:
                docs = json.load(f)
                documents.extend(docs)

    # Upsert to Pinecone
    vectors = []
    for doc in documents:
        embedding = get_embedding(doc["text"])
        vectors.append((doc["id"], embedding, {"title": doc["title"], "source": doc["source"], "text": doc["text"]}))

    if vectors:
        index.upsert(vectors)
        print(f"Indexed {len(vectors)} documents into Pinecone.")
    else:
        print("No documents found to index.")

if __name__ == "__main__":
    index_kb()
