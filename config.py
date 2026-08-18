"""
Central configuration for GPU Scout.
Keeping these values in one place means you only edit them here,
not hunt through every file that touches the LLM or the vector DB.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM (cloud, via Groq) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# --- Embeddings (local, via Ollama) ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
DB_DIR = os.path.join(BASE_DIR, "gpu_db")

# --- Retrieval ---
RETRIEVAL_K = 5

# --- Memory ---
MEMORY_TURNS = 3            # how many past Q&A pairs go into each LLM prompt
MEMORY_DB_PATH = os.path.join(BASE_DIR, "memory.db")  # persistent, cross-session storage
MEMORY_DISPLAY_LIMIT = 20   # how many past turns to reload into the UI on startup

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add it to your .env file "
        "(see .env.example)."
    )
