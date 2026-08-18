from experts.expert import Expert

professional = Expert(
    role="Professional Workloads Expert",
    specialties="""
- Blender and 3D rendering
- Unreal Engine and other game engines
- CAD software
- Video editing (Premiere, DaVinci Resolve, After Effects)
- CUDA-accelerated professional applications
""",
)


def answer_professional_question(question, history=None, verbose=False):
    return professional.answer(question, history=history, verbose=verbose)
