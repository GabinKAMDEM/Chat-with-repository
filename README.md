# Chat-with-Repository

> **Conversation-driven code explorer**  
> RAG + LangChain + Chroma + Streamlit • Docker-ready 

---

##  Features

| Category | What it does |
|----------|--------------|
| **Project summary** | Clones the repo, chunk-splits README & code, embeds every chunk → generates an “executive summary”. |
| **Module / symbol explorer** | Static AST parser lists every module → class → function; one-click signature + docstring + LLM explanation in UI. |
| **Conversational RAG agent** | LangGraph picks the right chain:<br>• *summary* – global overview<br>•  *qa_node* – open Q/A with chat memory.<br>Answers are contextualised & cited. |
| **Embeddings store** | Chroma (DuckDB+Parquet) persisted. |
| **Hot re-index** | From the sidebar you paste any Git URL → click **Index & start chat** → ingestion → embeddings → chat ready. |

---
## Quick start (local)

```bash
git clone https://github.com/you/chat-with-repo.git
cd chat-with-repo
python -m venv .venv && source .venv/bin/activate

cp .env.example .env          # fill OPENAI_API_KEY
pip install -e .

streamlit run app/app.py      # open http://localhost:8501

```
Paste a Git URL, click Index & start chat, wait a few seconds, enjoy the chat.

---
## Environment variables
Key and Description

```text
OPENAI_API_KEY	Your OpenAI key (required).
LLM_MODEL	Chat model default gpt-4.o-mini.
EMBEDDING_MODEL	Embeddings, default text-embedding-3-small.
CHROMA_COLLECTION	Collection name (default repo_index).
```