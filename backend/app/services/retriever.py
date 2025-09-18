from app.services.embeddings import get_embedding
from app.services.pinecone_client import get_index

def retrieve(query: str, top_k: int = 3):
    """Retrieve top-k relevant documents from Pinecone for a query."""
    index = get_index()

    # Convert query to embedding
    query_vector = get_embedding(query)

    # Query Pinecone
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    docs = []
    for match in results["matches"]:
        docs.append({
            "id": match["id"],
            "score": match["score"],
            "title": match["metadata"].get("title", ""),
            "source": match["metadata"].get("source", ""),
            "text": match["metadata"].get("text", "")
        })

    return docs

if __name__ == "__main__":
    # Quick test
    test_query = "What is Delivery Attempt Policy?"
    results = retrieve(test_query, top_k=2)
    for r in results:
        print(f"ID: {r['id']} | Score: {r['score']:.4f} | Title: {r['title']}")
        print(f"Text: {r['text']}\n")
