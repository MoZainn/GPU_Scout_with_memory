"""
Small shared helper for building the conversation-history text that gets
fed back into prompts (used by both router.py and experts/expert.py).
"""


def summarize_answer(answer, max_len=300):
    """
    Pull the most useful slice of a past answer for memory context.

    Expert prompts ask for reasoning followed by a final answer, so the
    actual conclusion usually sits at the END of the text. Naively slicing
    the first `max_len` characters cuts off exactly the part we need —
    the conclusion — and keeps only throwaway reasoning. This looks for
    the "Final Answer:" marker and anchors on that instead; if it's not
    found, it falls back to the TAIL of the string rather than the head,
    since the tail is still more likely to hold the conclusion.
    """
    marker = "final answer:"
    idx = answer.lower().rfind(marker)
    if idx != -1:
        return answer[idx:idx + max_len].strip()
    return answer[-max_len:].strip()
