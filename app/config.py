import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model_20241029_093521.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer_20241029_093521.joblib")
MAPPINGS_PATH = os.path.join(MODEL_DIR, "mappings_20241029_093521.json")

# API configurations
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))