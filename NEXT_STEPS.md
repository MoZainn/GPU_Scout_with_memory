# Next Steps (in order)

Everything below assumes you're running this on the machine where
Ollama is installed and working.

- [ ] **1. Rotate your Groq API key** (the old one leaked into this
      chat/upload — revoke it at https://console.groq.com and get a
      new one).
- [ ] **2. Unzip/copy this project**, then:
      ```bash
      cd gpu_scout
      pip install -r requirements.txt
      cp .env.example .env
      ```
      Paste your new key into `.env`.
- [ ] **3. Pull the embedding model** (skip if already pulled):
      ```bash
      ollama pull nomic-embed-text
      ```
- [ ] **4. Delete the old `gpu_db/` and rebuild it** — it was built
      with a broken ingest path before, and the `Data/` folder now
      has new gaming/hardware/professional content it never saw:
      ```bash
      rm -rf gpu_db
      python ingest.py
      ```
- [ ] **5. Smoke-test on the CLI first** (faster feedback loop than
      Streamlit while you're checking things work):
      ```bash
      python agent.py
      ```
      Try one question per category: a VRAM question, an LLM/AI
      question, a gaming FPS question, a PSU question, a Blender
      question. Confirm each routes where you expect.
- [ ] **6. Launch the web UI:**
      ```bash
      streamlit run app.py
      ```
- [ ] **7. (Optional, if time allows)** Add a few more `.md` files to
      `Data/gpu_specs/` for any specific GPUs you want the agent to
      know well, then re-run `python ingest.py`.

If something breaks, the most likely culprits, in order: Ollama not
running, the API key not set, or `gpu_db/` not rebuilt after adding
new `Data/` files.
