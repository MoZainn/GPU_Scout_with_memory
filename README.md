

https://github.com/user-attachments/assets/9499fe68-ee2b-455b-a35c-25c4a7492ed3

# GPU Scout

**Status: Prototype.** Working end-to-end, actively being extended. See
[Known limitations](#known-limitations--next-steps) for exactly what's
rough and what's next — no surprises if you dig into the code.

A multi-expert RAG agent that answers GPU questions — specs, gaming
performance, hardware builds, AI workloads, professional software — by
routing each question to the right specialist instead of one
undifferentiated prompt. Built with Groq (`llama-3.1-8b-instant`),
local Ollama embeddings, FAISS, and Streamlit.

## Why

Most "AI GPU advisor" demos are a single prompt with some product
data stuffed into context. That falls apart in two ways: retrieval
gets diluted across unrelated domains, and every question pays for an
LLM call even when a keyword would answer it faster and for free.
GPU Scout exists to try a cleaner version of that pattern.

The example I keep coming back to: ask it *"would an RTX 4090 run
GTA 6 well?"* — GTA 6 has no confirmed PC release or official specs
as of this writing. Instead of inventing a benchmark number, the
agent says so, explains why (Rockstar's historical console-to-PC gap),
and gives a clearly-labeled estimate instead of a fabricated fact.
That behavior comes from the retrieval design, not a smarter model.

## How it works

```
your question
      │
      ▼
  router.py  ──► keyword match? ──► yes ──► category
      │
      └──► no ──► LLM classifies ──► category
      │
      ▼
  agent.py routes to the matching expert
      │
      ▼
  expert retrieves top-k chunks from FAISS (Data/*.md)
      │
      ▼
  LLM answers using only that retrieved context
```

Five experts share one FAISS index: **specs**, **ai**, **gaming**,
**hardware**, **professional**. The category determines which expert
persona answers, not a hard data partition — any expert can retrieve
any document if it's relevant.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and paste in your own [Groq API key](https://console.groq.com).
Never commit `.env` — it's already in `.gitignore`.

### 3. Make sure Ollama is running with the embedding model

```bash
ollama pull nomic-embed-text
```

### 4. Build the vector database

```bash
python ingest.py
```

Run this again any time you add or edit files under `Data/`.

### 5. Run it

**Web UI:**
```bash
streamlit run app.py
```

**CLI** (quick testing without the browser):
```bash
python agent.py
```

## Project structure

```
gpu_scout/
├── app.py                    # Streamlit UI
├── agent.py                  # Core routing + answering logic (also runnable as CLI)
├── router.py                 # Keyword fast-path + LLM fallback classifier
├── config.py                 # All model names / paths in one place
├── ingest.py                 # Builds the FAISS DB from Data/
├── experts/
│   ├── expert.py              # Base Expert class (retrieve + answer)
│   ├── shared.py               # Shared LLM + FAISS DB instances
│   ├── ai_expert.py
│   ├── gaming_expert.py
│   ├── hardware_expert.py
│   ├── professional_expert.py
│   └── specs_expert.py
├── tools/
│   ├── gpu_specs.py           # Quick single-chunk spec lookup (no LLM call)
│   └── web_search.py          # Optional: search a live URL for extra context
└── Data/
    ├── ai/
    ├── gaming/
    ├── hardware/
    ├── professional/
    ├── gpu_specs/
    └── knowledge/
```

(`gpu_db/`, the generated FAISS index, is gitignored — build it
locally with `python ingest.py`.)

## Adding more knowledge

Drop a `.md` file into the relevant `Data/<category>/` folder, then
re-run `python ingest.py`.

## Known limitations / next steps

- Knowledge base is intentionally small right now — a handful of `.md`
  files per category, not a comprehensive GPU database.
- Retrieval is a flat top-k similarity search with no re-ranking and
  no per-category filtering, so closely related categories can
  occasionally pull overlapping context.
- No conversation memory — each question is answered independently.
  See `ARCHITECTURE.md` for where memory would plug in.
- `tools/web_search.py` is written but not wired into the main agent
  yet — for pulling in live web context when local retrieval is thin.
- No automated tests or eval harness yet.

None of these are hidden — see `ARCHITECTURE.md` for more on the
design decisions and what's planned.

## License

MIT — see [LICENSE](LICENSE).
