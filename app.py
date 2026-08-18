"""
GPU Scout — Streamlit UI.
Run with: streamlit run app.py
"""

import streamlit as st
from agent import gpu_agent
import config
import memory

st.set_page_config(page_title="GPU Scout", page_icon="▪", layout="centered")

# ---------------------------------------------------------------------------
# Visual identity: dark hardware-diagnostic aesthetic (think GPU-Z / MSI
# Afterburner readouts), not a generic chat-app skin. Monospace for labels
# and data, a clean sans face for prose, one accent per expert category so
# routing reads like a status LED rather than a text label.
# ---------------------------------------------------------------------------

CATEGORY_STYLE = {
    "specs":        {"color": "#6FD3FF", "label": "SPECS.SYS"},
    "ai":           {"color": "#B98CFF", "label": "AI.SYS"},
    "gaming":       {"color": "#00D9C0", "label": "GAMING.SYS"},
    "hardware":     {"color": "#FFB020", "label": "HARDWARE.SYS"},
    "professional": {"color": "#FF6F6F", "label": "PROFESSIONAL.SYS"},
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(0,217,192,0.06), transparent 45%),
            radial-gradient(circle at 85% 15%, rgba(185,140,255,0.05), transparent 40%),
            #0A0C0F;
    }

    /* ---- Header block ---- */
    .scout-header {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin-bottom: 2px;
    }
    .scout-title {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.9rem;
        letter-spacing: 0.5px;
        color: #E8ECF1;
        margin: 0;
    }
    .scout-title span {
        color: #00D9C0;
    }
    .scout-build {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #4A5566;
        letter-spacing: 1px;
    }
    .scout-subtitle {
        font-family: 'Inter', sans-serif;
        color: #7C8797;
        font-size: 0.92rem;
        margin-top: 4px;
        margin-bottom: 14px;
    }
    .circuit-divider {
        height: 2px;
        width: 100%;
        margin-bottom: 26px;
        background: repeating-linear-gradient(
            90deg,
            #00D9C0 0px, #00D9C0 6px,
            transparent 6px, transparent 14px
        );
        opacity: 0.55;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: #0D1015;
        border-right: 1px solid #1C222C;
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 1.5px;
        color: #00D9C0;
        text-transform: uppercase;
    }
    .sidebar-panel {
        background: #12161C;
        border: 1px solid #1C222C;
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 14px;
    }
    .sidebar-row {
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        padding: 3px 0;
        color: #A8B1BE;
    }
    .sidebar-row span:last-child {
        color: #E8ECF1;
    }

    /* ---- Chat bubbles ---- */
    div[data-testid="stChatMessage"] {
        background: #12161C !important;
        border: 1px solid #1C222C;
        border-radius: 8px;
    }

    /* ---- Routing badge ---- */
    .route-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 1px;
        padding: 3px 10px;
        border-radius: 4px;
        background: #0D1015;
        border: 1px solid #232A34;
        margin-bottom: 10px;
    }
    .route-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 6px currentColor;
    }

    /* ---- Chat input ---- */
    div[data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stChatInput"] {
        border: 1px solid #232A34 !important;
    }

    /* ---- Buttons / toggle ---- */
    button[kind="secondary"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="scout-header">
        <p class="scout-title">GPU <span>SCOUT</span></p>
        <span class="scout-build">v1.0 // multi-expert RAG</span>
    </div>
    <p class="scout-subtitle">
        Ask about specs, AI workloads, gaming performance, hardware builds, or
        professional software. Routed to the right specialist automatically.
    </p>
    <div class="circuit-divider"></div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Identity")
    st.caption(
        "A simple local ID used to save/reload your history across "
        "sessions — not a real login system."
    )
    user_id = st.text_input("User ID", value=st.session_state.get("user_id", "guest")).strip() or "guest"

# (Re)load history whenever the user_id changes, or on first run.
if st.session_state.get("user_id") != user_id:
    st.session_state.user_id = user_id
    st.session_state.history = memory.load_history(user_id, limit=config.MEMORY_DISPLAY_LIMIT)
elif "history" not in st.session_state:
    st.session_state.history = memory.load_history(user_id, limit=config.MEMORY_DISPLAY_LIMIT)

with st.sidebar:
    st.markdown("### Diagnostics")
    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-row"><span>ROUTER</span><span>keyword + LLM</span></div>
            <div class="sidebar-row"><span>RETRIEVAL</span><span>FAISS / top-k</span></div>
            <div class="sidebar-row"><span>EMBEDDINGS</span><span>local (Ollama)</span></div>
            <div class="sidebar-row"><span>LLM</span><span>Groq (cloud)</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Experts online")
    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-row"><span style="color:#6FD3FF">●</span><span>specs</span></div>
            <div class="sidebar-row"><span style="color:#B98CFF">●</span><span>ai</span></div>
            <div class="sidebar-row"><span style="color:#00D9C0">●</span><span>gaming</span></div>
            <div class="sidebar-row"><span style="color:#FFB020">●</span><span>hardware</span></div>
            <div class="sidebar-row"><span style="color:#FF6F6F">●</span><span>professional</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    verbose = st.toggle("Show retrieved context", value=False)
    if st.button("Clear conversation"):
        memory.clear_history(st.session_state.user_id)
        st.session_state.history = []
        st.rerun()


def render_badge(category):
    style = CATEGORY_STYLE.get(category, {"color": "#7C8797", "label": category.upper()})
    st.markdown(
        f"""
        <div class="route-badge" style="color:{style['color']}">
            <span class="route-dot" style="background:{style['color']}"></span>
            ROUTED &rarr; {style['label']}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Render past turns
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        render_badge(turn["category"])
        st.write(turn["answer"])

# New question
question = st.chat_input("Ask about a GPU, AI workload, game performance, or build...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Routing and thinking..."):
            try:
                category, answer = gpu_agent(
                    question, history=st.session_state.history, verbose=verbose
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        render_badge(category)
        st.write(answer)

    st.session_state.history.append(
        {"question": question, "category": category, "answer": answer}
    )
    memory.save_turn(st.session_state.user_id, question, category, answer)
