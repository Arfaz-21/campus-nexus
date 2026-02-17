import streamlit as st
from pypdf import PdfReader
import re
import math
from groq import Groq

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Campus Nexus – AI Academic Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #0b1629 100%);
    border-right: 1px solid #1e3a5f;
    min-width: 280px !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #38bdf8 !important;
}
section[data-testid="stSidebar"] .stTextInput {
    width: 100% !important;
}
section[data-testid="stSidebar"] .stTextInput > div {
    width: 100% !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 0.75rem !important;
}
section[data-testid="stSidebar"] .stFileUploader {
    width: 100% !important;
}
section[data-testid="stSidebar"] .stFileUploader > div {
    width: 100% !important;
}

.hero-banner {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #8b5cf6 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    margin: 0.4rem 0 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stat-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    flex: 1 1 120px;
    min-width: 100px;
    background: linear-gradient(135deg, #0f2744 0%, #0c1f38 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    text-align: center;
}
.stat-number {
    font-size: 1.9rem;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.panel {
    background: linear-gradient(135deg, #0f2744 0%, #0c1f38 100%);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ai-answer-box {
    background: linear-gradient(135deg, #0c1f38, #0a1a30);
    border: 1px solid #0ea5e9;
    border-left: 4px solid #0ea5e9;
    border-radius: 12px;
    padding: 1.5rem;
    color: #e2e8f0;
    font-size: 0.95rem;
    line-height: 1.7;
    white-space: pre-wrap;
    margin: 1rem 0;
}

.evidence-box {
    background: #060d1a;
    border: 1px solid #1e3a5f;
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 1.2rem;
    color: #94a3b8;
    font-size: 0.85rem;
    font-family: 'Courier New', monospace;
    line-height: 1.6;
    margin: 0.75rem 0;
}

.conf-track {
    background: #0f2744;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 0.5rem 0;
}
.conf-fill-high   { height:100%; border-radius:999px; background: linear-gradient(90deg,#10b981,#34d399); }
.conf-fill-medium { height:100%; border-radius:999px; background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.conf-fill-low    { height:100%; border-radius:999px; background: linear-gradient(90deg,#ef4444,#f87171); }

.chip {
    display: inline-block;
    border-radius: 20px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
}
.chip-high   { background: rgba(16,185,129,0.15); color:#34d399; border:1px solid rgba(52,211,153,0.3); }
.chip-medium { background: rgba(245,158,11,0.15);  color:#fbbf24; border:1px solid rgba(251,191,36,0.3); }
.chip-low    { background: rgba(239,68,68,0.15);   color:#f87171; border:1px solid rgba(248,113,113,0.3); }

.history-item {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.history-q { color:#38bdf8; font-size:0.85rem; font-weight:600; margin-bottom:0.4rem; }
.history-a { color:#94a3b8; font-size:0.82rem; line-height:1.5; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0a1628 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 2px rgba(14,165,233,0.15) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100%;
    transition: opacity 0.2s;
}
div.stButton > button:hover { opacity: 0.9; }

.stSelectbox > div > div {
    background: #0a1628 !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

.stSpinner > div { border-top-color: #0ea5e9 !important; }

.streamlit-expanderHeader {
    background: #0f2744 !important;
    color: #38bdf8 !important;
    border-radius: 10px !important;
    border: 1px solid #1e3a5f !important;
}

hr { border-color: #1e3a5f !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "history"       not in st.session_state: st.session_state.history       = []
if "chunks"        not in st.session_state: st.session_state.chunks        = []
if "pages_data"    not in st.session_state: st.session_state.pages_data    = []
if "groq_ready"  not in st.session_state: st.session_state.groq_ready  = False
if "api_key"       not in st.session_state: st.session_state.api_key       = ""
if "doc_name"      not in st.session_state: st.session_state.doc_name      = ""
if "source_files"  not in st.session_state: st.session_state.source_files  = []
if "manual_chunk"  not in st.session_state: st.session_state.manual_chunk  = 350
if "manual_topk"   not in st.session_state: st.session_state.manual_topk   = 4


# ─────────────────────────────────────────────
# INGESTION
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def extract_text_with_pages(pdf_file):
    pages_data = []
    reader = PdfReader(pdf_file)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages_data.append({"page": i + 1, "content": text.strip(), "source_file": ""})
    return pages_data


# ─────────────────────────────────────────────
# CHUNKING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def chunk_text(pages_data_frozen, overlap=50, manual_chunk_size=0):
    pages_data = [dict(p) for p in pages_data_frozen]
    if manual_chunk_size > 0:
        chunk_size = manual_chunk_size
    else:
        total_words = sum(len(p["content"].split()) for p in pages_data)
        if total_words < 2000:
            chunk_size = 200
        elif total_words < 10000:
            chunk_size = 350
        else:
            chunk_size = 500

    chunks = []
    for item in pages_data:
        # Split by paragraph breaks first — keeps sentences intact
        paragraphs = [p.strip() for p in re.split(r'\n{2,}', item["content"]) if p.strip()]

        # If paragraphs are too short (e.g. single-line PDF), fall back to word-based
        if len(paragraphs) <= 2:
            paragraphs = [item["content"]]

        buffer = []
        buffer_words = 0
        for para in paragraphs:
            para_words = para.split()
            # If adding this paragraph exceeds chunk_size, flush buffer first
            if buffer_words + len(para_words) > chunk_size and buffer:
                chunks.append({
                    "page":        item["page"],
                    "content":     " ".join(buffer),
                    "source_file": item.get("source_file", "")
                })
                # Keep last sentence as overlap context
                overlap_text = " ".join(buffer[-overlap:]) if len(buffer) > overlap else " ".join(buffer)
                buffer = overlap_text.split()
                buffer_words = len(buffer)
            buffer.extend(para_words)
            buffer_words += len(para_words)

        # Flush remaining buffer
        if buffer:
            chunks.append({
                "page":        item["page"],
                "content":     " ".join(buffer),
                "source_file": item.get("source_file", "")
            })
    return chunks


# ─────────────────────────────────────────────
# TF-IDF RETRIEVAL
# ─────────────────────────────────────────────
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    stopwords = {"the","a","an","is","it","in","on","at","to","of","for",
                 "and","or","but","with","this","that","are","was","were",
                 "be","been","being","have","has","had","do","does","did",
                 "will","would","could","should","may","might","shall","can",
                 "not","no","from","by","as","we","i","you","he","she","they"}
    return [t for t in tokens if t not in stopwords and len(t) > 1]

def tfidf_score(query_tokens, chunk_content, all_chunks):
    chunk_tokens = preprocess(chunk_content)
    if not chunk_tokens or not query_tokens:
        return 0.0
    N = len(all_chunks)
    score = 0.0
    for term in query_tokens:
        tf = chunk_tokens.count(term) / len(chunk_tokens)
        df = sum(1 for c in all_chunks if term in preprocess(c["content"]))
        idf = math.log((N + 1) / (df + 1)) + 1
        score += tf * idf
    return score

def get_top_chunks(query, chunks, top_k=4):
    query_tokens = preprocess(query)
    if not query_tokens:
        return [], [], []
    scored = []
    for chunk in chunks:
        s = tfidf_score(query_tokens, chunk["content"], chunks)
        scored.append((s, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [(s, c) for s, c in scored[:top_k] if s > 0]
    if not top:
        return [], query_tokens, []
    max_s = top[0][0]
    normalised = [(min(s / max_s, 1.0), c) for s, c in top]
    top_chunk_tokens = set(preprocess(top[0][1]["content"]))
    matched = [t for t in query_tokens if t in top_chunk_tokens]
    return normalised, query_tokens, matched


# ─────────────────────────────────────────────
# GROQ AI ANSWER
# ─────────────────────────────────────────────
def ask_groq(api_key, query, context_chunks):
    client = Groq(api_key=api_key)
    context = "\n\n".join(
        f"[File: {c.get('source_file', 'unknown')} | Page {c['page']}]\n{c['content']}" for _, c in context_chunks
    )
    prompt = f"""You are Campus Nexus, a precise and trustworthy academic assistant.
A student has asked a question about their academic document.

Your task:
1. Answer ONLY using the document excerpts provided below. Do not use outside knowledge.
2. If the answer is clearly present, give a direct, well-structured response.
3. If the answer is partially present, state what the document says and flag what is missing.
4. If the answer is not in the excerpts at all, explicitly say: "This information was not found in the provided document."
5. Always cite the source file and page number when referencing specific content.
6. Be concise, accurate, and student-friendly. Avoid filler phrases.

--- DOCUMENT EXCERPTS ---
{context}
--- END EXCERPTS ---

Student Question: {query}

Answer:"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Campus Nexus")
    st.markdown("<div style='color:#64748b;font-size:0.8rem;margin-bottom:1.5rem;'>AI Academic Assistant</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🔑 Groq API Key")
    st.markdown(
        "<p style='color:#64748b;font-size:0.78rem;margin:0 0 0.5rem;line-height:1.5;'>"
        "Free key at <b style='color:#94a3b8;'>console.groq.com</b><br>"
        "<span style='font-size:0.72rem;'>Sign up → API Keys → Create Key</span></p>",
        unsafe_allow_html=True
    )
    api_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed",
        key="api_key_input"
    )
    if api_input:
        st.session_state.api_key = api_input
        st.session_state.groq_ready = True
        st.markdown(
            "<div style='background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);"
            "border-radius:8px;padding:0.4rem 0.75rem;margin-top:0.4rem;'>"
            "<span style='color:#34d399;font-size:0.82rem;font-weight:600;'>✅ API key saved</span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.25);"
            "border-radius:8px;padding:0.4rem 0.75rem;margin-top:0.4rem;'>"
            "<span style='color:#f87171;font-size:0.8rem;'>⚠️ Required for AI answers</span>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 📄 Upload Document")
    st.markdown(
        "<p style='color:#64748b;font-size:0.78rem;margin:0 0 0.5rem;'>Upload any academic PDF</p>",
        unsafe_allow_html=True
    )
    uploaded_files = st.file_uploader("Upload PDF", type="pdf",
                                       accept_multiple_files=True,
                                       label_visibility="collapsed")

    if uploaded_files:
        current_names = sorted([f.name for f in uploaded_files])
        if current_names != st.session_state.source_files:
            with st.spinner(f"Ingesting {len(uploaded_files)} document(s)…"):
                all_pages = []
                warned    = []
                for f in uploaded_files:
                    file_pages = extract_text_with_pages(f)
                    if len(file_pages) > 500:
                        file_pages = file_pages[:500]
                        warned.append(f.name)
                    for p in file_pages:
                        p["source_file"] = f.name
                    all_pages.extend(file_pages)
                st.session_state.pages_data   = all_pages
                st.session_state.chunks = chunk_text(
                    tuple(frozenset(p.items()) for p in all_pages),
                    overlap=50,
                    manual_chunk_size=st.session_state.manual_chunk
                )
                st.session_state.doc_name     = current_names[0]
                st.session_state.source_files = current_names
                st.session_state.history      = []
                if warned:
                    st.warning(f"⚠️ Large file(s) detected: {', '.join(warned)} — capped at 500 pages each.")

        pages  = len(st.session_state.pages_data)
        chunks = len(st.session_state.chunks)
        words  = sum(len(p["content"].split()) for p in st.session_state.pages_data)
        n_docs = len(st.session_state.source_files)

        st.markdown(f"""
        <div style='background:#060d1a;border:1px solid #1e3a5f;border-radius:10px;padding:1rem;margin-top:0.5rem;'>
            <div style='color:#34d399;font-size:0.82rem;font-weight:600;margin-bottom:0.75rem;'>✅ {n_docs} Document(s) Loaded</div>
            <div style='color:#94a3b8;font-size:0.78rem;'>📂 <b style="color:#e2e8f0">{n_docs}</b> files</div>
            <div style='color:#94a3b8;font-size:0.78rem;'>📋 <b style="color:#e2e8f0">{pages}</b> pages</div>
            <div style='color:#94a3b8;font-size:0.78rem;'>🔲 <b style="color:#e2e8f0">{chunks}</b> chunks indexed</div>
            <div style='color:#94a3b8;font-size:0.78rem;'>📝 <b style="color:#e2e8f0">{words:,}</b> words ingested</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 Pipeline")
    stages = [
        ("📥", "PDF Ingestion",    bool(st.session_state.pages_data)),
        ("🔲", "Chunking",         bool(st.session_state.chunks)),
        ("🔍", "TF-IDF Retrieval", bool(st.session_state.chunks)),
        ("🤖", "Groq AI Answer",   st.session_state.groq_ready),
        ("✅", "Verification",     st.session_state.groq_ready),
    ]
    for icon, label, done in stages:
        color  = "#34d399" if done else "#334155"
        bullet = "●" if done else "○"
        st.markdown(f"<div style='color:{color};font-size:0.82rem;padding:0.2rem 0;'>{bullet} {icon} {label}</div>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Retrieval Settings")
    st.markdown("<p style='color:#64748b;font-size:0.75rem;margin:0 0 0.5rem;'>Override adaptive defaults</p>", unsafe_allow_html=True)
    manual_chunk = st.slider("Chunk Size (words)", min_value=100, max_value=600, value=350, step=50)
    manual_topk  = st.slider("Top-K Chunks", min_value=1, max_value=8, value=4, step=1)
    st.session_state.manual_chunk = manual_chunk
    st.session_state.manual_topk  = manual_topk


# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✦ InnovGenius Hackathon — Round 2</div>
    <p class="hero-title">🚀 Campus Nexus</p>
    <p class="hero-sub">AI-Powered Academic Intelligence &nbsp;·&nbsp; PDF Ingestion &rarr; TF-IDF Retrieval &rarr; Groq AI Reasoning &rarr; Verified Answers</p>
</div>
""", unsafe_allow_html=True)

total_q      = len(st.session_state.history)
total_pages  = len(st.session_state.pages_data)
total_chunks = len(st.session_state.chunks)
ai_status    = "Active" if st.session_state.groq_ready else "Offline"

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.source_files) if st.session_state.source_files else total_pages}</div>
        <div class="stat-label">{'Docs Loaded' if st.session_state.source_files else 'Pages Indexed'}</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{total_chunks}</div>
        <div class="stat-label">Chunks Ready</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{total_q}</div>
        <div class="stat-label">Queries Run</div>
    </div>
    <div class="stat-card">
        <div class="stat-number" style="color:{'#34d399' if st.session_state.groq_ready else '#f87171'};">{ai_status}</div>
        <div class="stat-label">Groq AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🧠  Ask the Document", "📄  Document Explorer", "📜  Query History"])

# ── TAB 1 ──
with tab1:
    if not st.session_state.chunks:
        st.markdown("""
        <div style='text-align:center;padding:3rem;'>
            <div style='font-size:3rem;'>📂</div>
            <div style='font-size:1.1rem;margin-top:0.75rem;color:#64748b;'>Upload a PDF in the sidebar to get started</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_q, col_hint = st.columns([3, 1])
        with col_q:
            user_query = st.text_input(
                "Ask anything about your document",
                placeholder="e.g. What are the key research findings?",
                label_visibility="visible"
            )
        with col_hint:
            mode = st.selectbox("Mode", ["🤖 AI Answer", "🔍 Retrieval Only"], label_visibility="visible")

        submit = st.button("⚡ Submit Query")

        if submit and user_query.strip():
            top_chunks, query_tokens, matched_terms = get_top_chunks(
                user_query, st.session_state.chunks,
                top_k=st.session_state.manual_topk
            )

            if not top_chunks:
                st.error("No relevant content found. Try rephrasing your query.")
            else:
                conf_score = top_chunks[0][0]
                best_chunk = top_chunks[0][1]

                left, right = st.columns([3, 2], gap="large")

                with left:
                    st.markdown('<div class="panel-title">🤖 AI-Generated Answer</div>', unsafe_allow_html=True)

                    ai_answer = None
                    if "AI Answer" in mode and st.session_state.groq_ready:
                        with st.spinner("Groq AI is reasoning over your document…"):
                            try:
                                ai_answer = ask_groq(st.session_state.api_key, user_query, top_chunks)
                                st.markdown(f'<div class="ai-answer-box">{ai_answer}</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Groq error: {e}")
                                ai_answer = None
                    elif "AI Answer" in mode and not st.session_state.groq_ready:
                        st.warning("Add your Groq API key in the sidebar to enable AI answers.")
                    else:
                        # Retrieval Only — synthesize a readable answer from top chunks
                        combined = " ".join(c["content"] for _, c in top_chunks[:2])
                        sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', combined) if len(s.strip()) > 40]
                        summary = " ".join(sentences[:5]) if sentences else combined[:500]
                        st.markdown(
                            f'<div class="ai-answer-box" style="border-color:#6366f1;border-left-color:#6366f1;">'
                            f'<span style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">Retrieval Summary (no AI)</span><br><br>'
                            f'{summary}…'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown('<div class="panel-title" style="margin-top:1.25rem;">📌 Top Retrieved Evidence</div>', unsafe_allow_html=True)
                    for rank, (score, chunk) in enumerate(top_chunks, 1):
                        with st.expander(f"#{rank} — Page {chunk['page']}  ·  relevance {score*100:.0f}%"):
                            st.markdown(f'<div class="evidence-box">{chunk["content"][:600]}…</div>', unsafe_allow_html=True)

                with right:
                    st.markdown('<div class="panel-title">✅ Trust-Verify Dashboard</div>', unsafe_allow_html=True)

                    pct = conf_score * 100
                    fill_class = ("conf-fill-high" if pct >= 65 else "conf-fill-medium" if pct >= 35 else "conf-fill-low")
                    chip_class = ("chip-high" if pct >= 65 else "chip-medium" if pct >= 35 else "chip-low")
                    status_txt = ("HIGH CONFIDENCE" if pct >= 65 else "MEDIUM — REVIEW RECOMMENDED" if pct >= 35 else "LOW GROUNDING")

                    st.markdown(f"""
                    <div style='margin-bottom:1.25rem;'>
                        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;'>
                            <span style='color:#94a3b8;font-size:0.82rem;'>Retrieval Confidence</span>
                            <span style='color:#e2e8f0;font-weight:700;'>{pct:.1f}%</span>
                        </div>
                        <div class='conf-track'><div class='{fill_class}' style='width:{pct}%'></div></div>
                        <div style='margin-top:0.5rem;'><span class='chip {chip_class}'>{status_txt}</span></div>
                        <div style='margin-top:0.5rem;color:#475569;font-size:0.73rem;font-style:italic;'>
                            Normalised TF-IDF relevance score of top retrieved chunk
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    matched_str   = ", ".join(matched_terms) if matched_terms else "none"
                    unmatched_str = ", ".join([t for t in query_tokens if t not in matched_terms]) if query_tokens else ""
                    match_pct = int(len(matched_terms) / len(query_tokens) * 100) if query_tokens else 0

                    st.markdown(f"""
                    <div style='background:#060d1a;border:1px solid #1e3a5f;border-radius:10px;padding:1rem;margin-bottom:0.75rem;'>
                        <div style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.6rem;'>
                            Term Grounding Analysis
                        </div>
                        <div style='color:#94a3b8;font-size:0.8rem;margin-bottom:0.35rem;'>
                            Query tokens: <b style='color:#e2e8f0;'>{len(query_tokens)}</b>
                            &nbsp;|&nbsp; Matched: <b style='color:#34d399;'>{len(matched_terms)}</b>
                            &nbsp;|&nbsp; Coverage: <b style='color:#38bdf8;'>{match_pct}%</b>
                        </div>
                        <div style='background:#0a1628;border:1px solid #1e3a5f;border-radius:6px;padding:0.6rem 0.8rem;margin-top:0.4rem;font-family:monospace;font-size:0.8rem;'>
                            <span style='color:#64748b;'>Matched Terms: </span>
                            <span style='color:#34d399;font-weight:600;'>{matched_str}</span>
                        </div>
                        {f'<div style="margin-top:0.4rem;background:#0a1628;border:1px solid #1e3a5f;border-radius:6px;padding:0.5rem 0.8rem;font-family:monospace;font-size:0.78rem;"><span style="color:#64748b;">Not matched: </span><span style="color:#f87171;">{unmatched_str}</span></div>' if unmatched_str else ''}
                    </div>
                    """, unsafe_allow_html=True)

                    if pct < 30:
                        st.markdown("""
                        <div style='background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);border-left:4px solid #ef4444;border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.75rem;'>
                            <div style='color:#f87171;font-size:0.85rem;font-weight:600;margin-bottom:0.25rem;'>Responsible AI Warning</div>
                            <div style='color:#fca5a5;font-size:0.8rem;line-height:1.5;'>Answer may not be strongly grounded in this document. Confidence is below 30% — verify manually before relying on this response.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif pct < 65:
                        st.markdown("""
                        <div style='background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-left:4px solid #f59e0b;border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.75rem;'>
                            <div style='color:#fbbf24;font-size:0.82rem;font-weight:600;margin-bottom:0.2rem;'>Review Recommended</div>
                            <div style='color:#fcd34d;font-size:0.78rem;line-height:1.5;'>Moderate grounding detected. Cross-check against source pages cited below.</div>
                        </div>
                        """, unsafe_allow_html=True)

                    pages_used   = sorted(set(c["page"] for _, c in top_chunks))
                    pages_str    = ", ".join(map(str, pages_used))
                    sources_used = sorted(set(c.get("source_file", "unknown") for _, c in top_chunks))
                    sources_str  = ", ".join(sources_used)
                    st.markdown(f"""
                    <div style='background:#060d1a;border:1px solid #1e3a5f;border-radius:10px;padding:1rem;'>
                        <div style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.75rem;'>Source Metadata</div>
                        <div style='color:#94a3b8;font-size:0.83rem;margin-bottom:0.4rem;'>📂 Source files: <b style='color:#e2e8f0;'>{sources_str}</b></div>
                        <div style='color:#94a3b8;font-size:0.83rem;margin-bottom:0.4rem;'>📄 Source pages: <b style='color:#e2e8f0;'>{pages_str}</b></div>
                        <div style='color:#94a3b8;font-size:0.83rem;margin-bottom:0.4rem;'>🔲 Chunks retrieved: <b style='color:#e2e8f0;'>{len(top_chunks)}</b></div>
                        <div style='color:#94a3b8;font-size:0.83rem;margin-bottom:0.4rem;'>🔍 Retrieval method: <b style='color:#e2e8f0;'>TF-IDF</b></div>
                        <div style='color:#94a3b8;font-size:0.83rem;'>🤖 Answer model: <b style='color:#e2e8f0;'>{'Groq LLaMA 3.3 70B' if ai_answer else 'Retrieval Only'}</b></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-top:0.75rem;'>
                        <div style='background:#060d1a;border:1px solid #1e3a5f;border-radius:10px;padding:0.85rem;text-align:center;'>
                            <div style='font-size:1.4rem;font-weight:700;color:#38bdf8;'>{len(top_chunks)}</div>
                            <div style='font-size:0.7rem;color:#64748b;text-transform:uppercase;'>Chunks Used</div>
                        </div>
                        <div style='background:#060d1a;border:1px solid #1e3a5f;border-radius:10px;padding:0.85rem;text-align:center;'>
                            <div style='font-size:1.4rem;font-weight:700;color:#6366f1;'>{len(pages_used)}</div>
                            <div style='font-size:0.7rem;color:#64748b;text-transform:uppercase;'>Pages Cited</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.session_state.history.append({
                    "query":      user_query,
                    "answer":     ai_answer or best_chunk["content"][:300],
                    "confidence": pct,
                    "pages":      pages_str,
                    "sources":    sources_str,
                    "ai_used":    ai_answer is not None,
                })


# ── TAB 2 ──
with tab2:
    if not st.session_state.pages_data:
        st.markdown("<div style='color:#64748b;text-align:center;padding:2rem;'>No document loaded yet.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#64748b;font-size:0.85rem;margin-bottom:1rem;'>Showing all {len(st.session_state.pages_data)} pages · {len(st.session_state.chunks)} total chunks</div>", unsafe_allow_html=True)
        for p in st.session_state.pages_data:
            word_count = len(p["content"].split())
            file_label = f" · {p.get('source_file', '')}" if p.get('source_file') else ""
            with st.expander(f"📄 Page {p['page']}{file_label}  ·  {word_count} words"):
                st.markdown(f'<div class="evidence-box" style="max-height:300px;overflow-y:auto;">{p["content"]}</div>', unsafe_allow_html=True)


# ── TAB 3 ──
with tab3:
    if not st.session_state.history:
        st.markdown("<div style='color:#64748b;text-align:center;padding:2rem;'>No queries yet. Ask something in the first tab!</div>", unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history), 1):
            pct = item["confidence"]
            chip_class = ("chip-high" if pct >= 65 else "chip-medium" if pct >= 35 else "chip-low")
            ai_tag = "Groq LLaMA 3.3 70B" if item["ai_used"] else "Retrieval Only"
            st.markdown(f"""
            <div class="history-item">
                <div class="history-q">Q{i}: {item['query']}</div>
                <div class="history-a">{item['answer'][:400]}{'…' if len(item['answer']) > 400 else ''}</div>
                <div style='margin-top:0.6rem;display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap;'>
                    <span class='chip {chip_class}' style='font-size:0.72rem;padding:0.2rem 0.7rem;'>{pct:.0f}% confidence</span>
                    <span style='color:#64748b;font-size:0.75rem;'>📄 Pages: {item['pages']}</span>
                    <span style='color:#64748b;font-size:0.75rem;'>📂 {item.get('sources', '—')}</span>
                    <span style='color:#64748b;font-size:0.75rem;'>{ai_tag}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#334155;font-size:0.78rem;padding:0.5rem 0 1rem;'>
    Campus Nexus &nbsp;·&nbsp; PDF Ingestion → TF-IDF Retrieval → Groq AI Reasoning → Trust Verification
    <br><span style='color:#1e3a5f;'>Built for InnovGenius Hackathon · Round 2</span>
</div>
""", unsafe_allow_html=True)