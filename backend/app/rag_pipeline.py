from typing import List, Dict
from app.services.retriever import retrieve
from app.services.llm_client import generate_response

def build_prompt(query: str, retrieved_docs: List[Dict]) -> str:
    """Construct a professional prompt for the LLM using retrieved docs."""
    context = ""
    for doc in retrieved_docs:
        context += f"- {doc['text']}\n"

    prompt = f"""
You are a professional customer support assistant for a logistics company.
Use the context provided below to answer the user's question.
Always give precise, professional, and concise answers.
Do NOT mention 'sources' or reveal internal document details.
If the answer is not in the documents, politely say you don’t have that information.

Context:
{context}

User Question:
{query}

Answer:
"""
    return prompt.strip()


def answer_query(query: str, top_k: int = 3) -> Dict:
    """Full RAG pipeline: retrieve → build prompt → LLM → answer."""
    # Step 1: Retrieve docs
    retrieved_docs = retrieve(query, top_k=top_k)

    # Step 2: Build prompt
    prompt = build_prompt(query, retrieved_docs)

    # Step 3: Get response from LLM
    llm_answer = generate_response(prompt)

    return {
        "query": query,
        "answer": llm_answer,
        "sources": retrieved_docs
    }

if __name__ == "__main__":
    test_query = "How can I track my parcel?"
    result = answer_query(test_query, top_k=2)
    print("\n=== User Query ===")
    print(result["query"])
    print("\n=== LLM Answer ===")
    print(result["answer"])
    print("\n=== Sources Used ===")
    for src in result["sources"]:
        print(f"- {src['title']} ({src['id']}) Score: {src['score']:.4f}")
