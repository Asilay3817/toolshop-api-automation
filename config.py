import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "")
TIMEOUT: float = float(os.getenv("TIMEOUT", "15"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", "logs/test.log")

if not BASE_URL:
    raise ValueError("URL не задан в .env")