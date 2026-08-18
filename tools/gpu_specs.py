"""
Lightweight lookup tool: returns the single best-matching chunk
for a quick spec question, without going through an expert/LLM call.
"""

from experts.shared import db


def get_gpu_specs(query):
    docs = db.similarity_search(query, k=1)
    if not docs:
        return "No matching GPU spec found."
    return docs[0].page_content
