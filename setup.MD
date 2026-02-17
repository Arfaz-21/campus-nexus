# 🚀 Campus Nexus — Round 2 Setup Guide

> **Campus Nexus** is a multi-document AI academic assistant that transforms fragmented academic PDFs into a unified, searchable knowledge system using TF-IDF retrieval and grounded LLM reasoning.

---

## Step 1: Install dependencies
```
pip install -r requirements.txt
```
That installs: `streamlit`, `pypdf`, `groq`

---

## Step 2: Get your FREE Groq API Key (2 minutes)
1. Go to → **https://console.groq.com**
2. Sign up with Google or email (free, no credit card)
3. Click **API Keys** in the left sidebar → **Create API Key**
4. Copy the key (starts with `gsk_...`)

> ✅ Free tier = 14,400 requests/day — no quota issues during demo

---

## Step 3: Run the app
```
py -m streamlit run app.py
```

---

## Step 4: Using the app

### Sidebar (do this first)
1. Paste your `gsk_...` key in the **🔑 Groq API Key** field → shows ✅ API key saved
2. Upload one or more academic PDFs — sidebar shows pages, chunks, words ingested
3. Adjust **⚙️ Retrieval Settings** sliders if needed (optional)

### Tab 1 — Ask the Document
- Type any question about your PDF
- Select mode:
  - **🤖 AI Answer** — Groq LLaMA 3.3 70B generates a full answer grounded in your document
  - **🔍 Retrieval Only** — synthesizes a summary from top chunks without using the API
- Hit **⚡ Submit Query**
- Results show: AI answer + top evidence chunks + Trust-Verify dashboard

### Tab 2 — Document Explorer
- Browse every page of your uploaded PDF(s)
- Each expander shows filename + page number + word count

### Tab 3 — Query History
- Every query saved with confidence score, source files, pages cited, and model used

---

## Demo Tips

**Show the Responsible AI trigger:**
Ask a question NOT in your document (e.g. "What is the capital of France?" on a physics PDF).
The confidence bar drops to red and shows **LOW GROUNDING** warning.
Tell judges: *"Unlike traditional AI systems, Campus Nexus does not fabricate answers. It explicitly signals when a query is not grounded in the uploaded documents."*

**Show multi-PDF retrieval:**
Upload 2 PDFs, ask a question. The Trust-Verify dashboard shows which file(s) the answer came from.

**Show retrieval sliders:**
Change Top-K from 4 to 2, resubmit. Show judges how retrieval depth affects results.

---

## What's upgraded from Round 1

| Feature | Round 1 | Round 2 |
|---|---|---|
| Retrieval | Keyword overlap (bag-of-words) | TF-IDF + paragraph-aware chunking |
| Chunking | Fixed 400-word splits | Paragraph-first, adaptive size, overlap |
| Answers | Raw chunk shown | Groq LLaMA 3.3 70B synthesized answer |
| Retrieval Only | Raw chunk dump | Synthesized summary from top chunks |
| Multi-PDF | ❌ | ✅ Unified corpus across all uploaded files |
| Source tracking | ❌ | ✅ File + page cited in every answer |
| UI | Single column | Tabs, stat cards, confidence meter, history |
| Evidence | 1 chunk | Top-K ranked chunks (adjustable via slider) |
| Confidence | Simple keyword match % | Normalised TF-IDF score with grounding warnings |
| Responsible AI | ❌ | ✅ Low/Medium/High grounding alerts |
| Caching | ❌ | ✅ `@st.cache_data` on ingestion + chunking |
| Large PDF guard | ❌ | ✅ Capped at 500 pages with warning |
| Retrieval settings | Hardcoded | ✅ Chunk size + Top-K sliders in sidebar |
| History | None | Full session history with metadata |
| Pipeline status | Hidden | Live indicator in sidebar |

---

**Architecture:** `PDF Ingestion → Paragraph-Aware Chunking → TF-IDF Retrieval → Groq LLaMA 3.3 70B Reasoning → Trust Verification Dashboard`