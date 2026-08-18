from experts.shared import db, llm
from memory_utils import summarize_answer
import config


class Expert:
    """
    Base class for a domain expert. Each expert retrieves the most
    relevant chunks from the shared vector DB, then asks the LLM to
    answer using only that context.
    """

    def __init__(self, role, specialties):
        self.role = role
        self.specialties = specialties

    def retrieve(self, question, k=config.RETRIEVAL_K):
        return db.similarity_search(question, k=k)

    @staticmethod
    def _format_history(history):
        if not history:
            return ""
        lines = ["Conversation so far:"]
        for turn in history[-config.MEMORY_TURNS:]:
            lines.append(f"User: {turn['question']}")
            lines.append(f"Assistant: {summarize_answer(turn['answer'])}")
        return "\n".join(lines) + "\n"

    def answer(self, question, history=None, verbose=False):
        docs = self.retrieve(question)

        if verbose:
            print("\nRetrieved Documents:\n")
            for i, doc in enumerate(docs):
                print(f"\n----- Document {i + 1} -----")
                print(doc.page_content[:700])

        context = "\n\n".join(doc.page_content for doc in docs)
        history_block = self._format_history(history)

        prompt = f"""You are GPU Scout's {self.role}.

You specialize in:
{self.specialties}

{history_block}
Use ONLY the provided context to answer factually. Use the conversation
history above only to resolve references like "it", "that one", or
"cheaper than what you said" — do not treat history as a source of GPU
facts. If the context does not contain enough information to answer
confidently, say so instead of guessing.

Context:
{context}

Current question:
{question}

Briefly explain your reasoning, then give a clear final answer.
"""

        response = llm.invoke(prompt)
        return response.content
