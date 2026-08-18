"""
Builds (or rebuilds) the FAISS vector database from every .md file
under Data/. Run this whenever you add or edit knowledge files.
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

import config

print(f"Loading documents from {config.DATA_DIR} ...")

loader = DirectoryLoader(
    config.DATA_DIR,
    glob="**/*.md",
    loader_cls=TextLoader,
)

documents = loader.load()
print(f"Loaded {len(documents)} documents")

if len(documents) == 0:
    raise RuntimeError(
        f"No .md files found under {config.DATA_DIR}. "
        "Check that your knowledge files exist there."
    )

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)
print(f"Created {len(docs)} chunks")

embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)

print("Creating embeddings (this calls your local Ollama server)...")
vectorstore = FAISS.from_documents(docs, embeddings)

print(f"Saving vector database to {config.DB_DIR} ...")
vectorstore.save_local(config.DB_DIR)

print("Done! You can now run the agent.")
