import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_URL = os.getenv("API_URL", f"http://localhost:{API_PORT}")

# Assets paths
IMAGE_DIR = BASE_DIR / "Image"
LOGO_PATH = IMAGE_DIR / "Logo.png"
INVERSE_LOGO_PATH = IMAGE_DIR / "inverseLogo.png"
