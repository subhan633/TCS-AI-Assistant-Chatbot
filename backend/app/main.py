from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, chat, admin

app = FastAPI(
    title="Customer Support Chatbot API",
    version="0.1.0",
    description="Backend for RAG-based TCS customer support chatbot"
)

# Allow frontend (Live Server) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Customer Support Chatbot Backend Running!"}
