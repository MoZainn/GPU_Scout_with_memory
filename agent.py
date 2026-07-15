"""
GPU Scout core agent.
Routes a question to the right expert and returns the answer.
This module has no UI code in it — app.py (Streamlit) and any
CLI wrapper both call gpu_agent() below.
"""

from router import route_question
from experts.ai_expert import answer_ai_question
from experts.gaming_expert import answer_gaming_question
from experts.hardware_expert import answer_hardware_question
from experts.professional_expert import answer_professional_question
from experts.specs_expert import answer_specs_question

EXPERTS = {
    "ai": answer_ai_question,
    "gaming": answer_gaming_question,
    "hardware": answer_hardware_question,
    "professional": answer_professional_question,
    "specs": answer_specs_question,
}


def gpu_agent(question, history=None, verbose=False):
    """
    Routes `question` to the correct expert and returns
    (category, answer_text). `history` is a list of past
    {"question": ..., "answer": ...} turns, used to resolve
    references like "that one" or "cheaper than what you said".
    """
    category = route_question(question, history=history)
    handler = EXPERTS.get(category, answer_specs_question)
    answer = handler(question, history=history, verbose=verbose)
    return category, answer


if __name__ == "__main__":
    print("GPU Scout (CLI mode). Type 'exit' to quit.\n")

    history = []

    while True:
        question = input("Ask GPU Scout: ").strip()

        if not question:
            continue
        if question.lower() == "exit":
            break

        category, answer = gpu_agent(question, history=history)

        print(f"\n[Routed to: {category} expert]\n")
        print(answer)
        print()

        history.append({"question": question, "answer": answer})
