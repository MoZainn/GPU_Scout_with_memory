from experts.expert import Expert

ai = Expert(
    role="AI Expert",
    specialties="""
- Local LLMs
- Machine Learning
- Deep Learning
- CUDA
- Stable Diffusion
- Tensor Cores
- Quantization
- AI inference and fine-tuning
""",
)


def answer_ai_question(question, history=None, verbose=False):
    return ai.answer(question, history=history, verbose=verbose)
