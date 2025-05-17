# Chat-with-Repository

> RAG chatbot pour interroger n’importe quel dépôt Git.

```bash
# local
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # renseigner OPENAI_API_KEY
streamlit run app/app.py
