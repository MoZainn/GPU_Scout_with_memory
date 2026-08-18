"""
Routes a user question to one of five expert categories:
specs, ai, gaming, hardware, professional.

Strategy:
1. Try a fast, free keyword match first (instant, no API call).
2. If nothing matches clearly, ask the LLM to classify (slower,
   but handles phrasing the keyword list didn't anticipate).
"""

from langchain_groq import ChatGroq
from memory_utils import summarize_answer
import config

VALID_CATEGORIES = {"specs", "ai", "gaming", "hardware", "professional"}

KEYWORDS = {
    "ai": [
        "llm", "ai", "stable diffusion", "deep learning", "machine learning",
        "cuda", "tensor", "mixtral", "llama", "chatgpt", "embedding",
        "quantization", "fine-tun", "inference",
    ],
    "gaming": [
        "fps", "gaming", "game", "ray tracing", "dlss", "fsr", "4k",
        "1080p", "1440p", "cyberpunk", "valorant", "fortnite",
    ],
    "hardware": [
        "power", "psu", "pcie", "motherboard", "cooling", "temperature",
        "cpu bottleneck", "airflow", "wattage",
    ],
    "professional": [
        "blender", "unreal engine", "cad", "premiere", "davinci",
        "after effects", "rendering", "render farm",
    ],
    "specs": [
        "vram", "cuda cores", "tensor cores", "rt cores", "clock speed",
        "memory bandwidth", "tdp", "architecture", "bus width",
    ],
}

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model_name=config.GROQ_MODEL,
            groq_api_key=config.GROQ_API_KEY,
        )
    return _llm


def _keyword_route(question):
    q = question.lower()
    scores = {cat: 0 for cat in KEYWORDS}

    for cat, words in KEYWORDS.items():
        for word in words:
            if word in q:
                scores[cat] += 1

    best_cat = max(scores, key=scores.get)

    if scores[best_cat] > 0:
        return best_cat
    return None


def _format_history(history):
    if not history:
        return ""
    lines = ["Recent conversation (for context only):"]
    for turn in history[-config.MEMORY_TURNS:]:
        lines.append(f"User: {turn['question']}")
        lines.append(f"Assistant: {summarize_answer(turn['answer'], max_len=200)}")
    return "\n".join(lines) + "\n"


def _llm_route(question, history=None):
    history_block = _format_history(history)
    prompt = f"""You are a routing expert for a GPU intelligence system.

{history_block}
Classify the user's CURRENT question into EXACTLY ONE category:

- specs: VRAM, CUDA cores, Tensor cores, clocks, TDP, architecture, memory bandwidth
- ai: LLMs, training, inference, Stable Diffusion, fine-tuning, CUDA
- gaming: FPS, DLSS, ray tracing, 1080p/1440p/4K
- hardware: PSU, CPU bottleneck, RAM, motherboard, power consumption
- professional: Blender, rendering, Unreal Engine, CAD, video editing

Use the conversation above only to resolve references (e.g. "that one",
"it", "cheaper than what you said") in the current question. Classify
based on the current question's actual subject matter.

Return ONLY the category name, nothing else.

Current question:
{question}
"""
    response = _get_llm().invoke(prompt)
    category = response.content.strip().lower()

    if category in VALID_CATEGORIES:
        return category
    return "specs"  # safe default


def route_question(question, history=None):
    category = _keyword_route(question)
    if category:
        return category
    return _llm_route(question, history=history)
