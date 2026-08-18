from experts.expert import Expert

hardware = Expert(
    role="Hardware Expert",
    specialties="""
- PSU sizing and power consumption
- Cooling and airflow
- CPU bottlenecks
- PCIe and motherboard compatibility
- System building
""",
)


def answer_hardware_question(question, history=None, verbose=False):
    return hardware.answer(question, history=history, verbose=verbose)
