"""
Optional tool: pulls a live web page, chunks it, and searches it for
relevant passages. NOT wired into the main agent by default — the
local knowledge base (Data/) is the primary source. Use this only if
you want to supplement an expert's answer with live web content.

Note: this needs outbound internet access and the `beautifulsoup4`
package (already in requirements.txt).
"""

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import config

embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def search_website(url, question, k=3):
    """
    Loads a single URL, splits it, and returns the top-k chunks
    most relevant to `question`. No recursion, no hardcoded URLs —
    call it once per source you actually want to check.
    """
    loader = WebBaseLoader(url)
    docs = loader.load()
    chunks = splitter.split_documents(docs)

    temp_db = FAISS.from_documents(chunks, embeddings)
    return temp_db.similarity_search(question, k=k)


def search_multiple(urls, question, k_per_site=3):
    """
    Searches several URLs and combines results. This is what the
    original code was trying to do (compare a given site against
    NVIDIA's CUDA docs) without the self-recursion bug.
    """
    all_docs = []
    for url in urls:
        all_docs.extend(search_website(url, question, k=k_per_site))
    return all_docs
