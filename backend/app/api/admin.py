import os
import json
from fastapi import APIRouter, UploadFile, File
from app.services.indexer import index_kb

router = APIRouter()

# Build path relative to backend/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "kb")

@router.post("/upload-kb")
async def upload_kb(file: UploadFile = File(...)):
    """Upload a new KB JSON file and re-index Pinecone."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Re-index after upload
    index_kb()
    return {"status": "success", "message": f"{file.filename} uploaded and KB re-indexed."}
