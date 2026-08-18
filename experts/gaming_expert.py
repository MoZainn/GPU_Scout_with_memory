from experts.expert import Expert

gaming = Expert(
    role="Gaming Expert",
    specialties="""
- Gaming performance (1080p, 1440p, 4K)
- FPS and frame generation
- DLSS / FSR
- Ray tracing
- Game optimization and settings
""",
)


def answer_gaming_question(question, history=None, verbose=False):
    return gaming.answer(question, history=history, verbose=verbose)
