"""
Shared resources for all experts: the LLM client and the vector DB.
Loaded once, imported everywhere, so we don't reconnect per-expert.
"""

import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

import config

embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)

if not os.path.isdir(config.DB_DIR):
    raise RuntimeError(
        f"No vector database found at '{config.DB_DIR}'.\n"
        "Run 'python ingest.py' first to build it from the Data/ folder."
    )

db = FAISS.load_local(
    config.DB_DIR,
    embeddings,
    allow_dangerous_deserialization=True,
)

llm = ChatGroq(
    model_name=config.GROQ_MODEL,
    groq_api_key=config.GROQ_API_KEY,
)
