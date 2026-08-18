from experts.expert import Expert

specs = Expert(
    role="GPU Specs Expert",
    specialties="""
- VRAM capacity and type
- CUDA cores, Tensor cores, RT cores
- Clock speeds and architecture
- Memory bandwidth and bus width
- TDP and power requirements
""",
)


def answer_specs_question(question, history=None, verbose=False):
    return specs.answer(question, history=history, verbose=verbose)
