from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.rag_pipeline import answer_query

router = APIRouter()

# Simple in-memory session store { session_id: [messages] }
SESSIONS = {}

class ChatRequest(BaseModel):
    session_id: str
    query: str
    history: List[Dict] = []  # optional: [{"role": "user", "content": "..."}]

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict]

@router.post("/")
def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id
    query = request.query

    # Get existing history or start new
    history = SESSIONS.get(session_id, [])
    history.append({"role": "user", "content": query})

    # Call RAG pipeline
    result = answer_query(query)

    # Save bot response in session
    history.append({"role": "assistant", "content": result["answer"]})
    SESSIONS[session_id] = history[-6:]  # keep last 6 turns

    return ChatResponse(answer=result["answer"], sources=result["sources"])
