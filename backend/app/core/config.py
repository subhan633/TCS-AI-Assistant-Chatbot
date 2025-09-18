import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Customer Support Chatbot"
    VERSION: str = "0.1.0"
    ENV: str = os.getenv("ENV", "development")

settings = Settings()
