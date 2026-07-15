# Architecture

## Design decisions

**Why keyword routing before LLM routing?**
Most GPU questions contain an obvious signal word ("fps", "vram",
"blender", "psu"). Catching those with a free, instant dictionary
lookup means only genuinely ambiguous questions ("which one is
better for me?") pay the cost of an extra LLM call. This is what
`router.py` does now — it replaces the two separate, conflicting
router implementations from the original prototype.

**Why one shared FAISS index instead of one per expert?**
Simpler to maintain, and a lot of GPU knowledge doesn't fit neatly
into one category anyway (e.g. "VRAM needed for Blender" touches
both `specs` and `professional`). Each expert just retrieves from
the same index with its own question — the "expert" difference is
in the system prompt/persona and framing, not a separate database.

**Why local embeddings (Ollama) + cloud LLM (Groq)?**
This was the original design and it's a reasonable split: embedding
generation runs constantly (every question, every ingest) and is
cheap to do locally with a small model; the actual reasoning/answer
generation benefits from a stronger hosted model. The tradeoff is
that Ollama must be running locally — documented in the README.

## What was broken in the original prototype, and why

| File | Problem | Fix |
|---|---|---|
| `ingest.py` | Loaded from `"data"` (lowercase); actual folder is `Data` | Case-correct path via `config.py` |
| `experts/ai_expert.py` etc. | `from expert import Expert` — bare import fails when loaded as `experts.ai_expert` | Changed to `from experts.expert import Expert`, added `experts/__init__.py` |
| `tools/web_search.py` | `search_website()` called itself inside its own body — infinite recursion | Removed self-call; added `search_multiple()` for the multi-source use case it was originally trying to do |
| `router.py` + `llm_router.py` | Two competing routers, different category sets, only one actually used | Merged into a single `router.py`: keyword fast-path, LLM fallback |
| `gpu_agent.py` + `gpu_agent_v2.py` | Two partial, overlapping entry points; `gpu_agent_v2.py` only wired up the AI expert | Merged into `agent.py`, wired to all 5 experts |
| `experts/professional_expert.py` | Referenced by the router's category list but the file didn't exist | Created |
| `experts/specs_expert.py` | Same — referenced but missing | Created |
| `Data/gaming`, `Data/hardware`, `Data/professional` | Empty folders — those experts had nothing dedicated to retrieve | Added baseline `.md` knowledge files |
| `app.py`, `requirements.txt` | Both empty | Built Streamlit UI and pinned dependency list |
| `.env` | Contained a live, exposed API key | Scrubbed and replaced with placeholder; added `.env.example` and `.gitignore` |

## Where to extend this later

- **Conversation memory**: `agent.py`'s `gpu_agent()` is stateless by
  design (easy to reason about, easy to test). To add memory, the
  natural place is to pass recent turns from `st.session_state.history`
  (already collected in `app.py`) into the expert's prompt in
  `experts/expert.py`.
- **Per-category retrieval filtering**: if `specs` and `ai` answers
  start bleeding into each other, tag each `Data/` file with metadata
  at ingest time and filter `db.similarity_search` by category.
- **Wiring in `tools/web_search.py`**: an expert could call it when
  local retrieval confidence is low, and merge the results into its
  context before answering.
