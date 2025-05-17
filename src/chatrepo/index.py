from chromadb import PersistentClient
from langchain_community.embeddings import OpenAIEmbeddings
from .config import DATA_DIR, settings
from .ingest import run_ingest

def build_index() -> None:
    docs = run_ingest()
    client = PersistentClient(path=str(DATA_DIR))
    collection = client.get_or_create_collection(settings.chroma_collection)

    embedder = OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)

    contents = [d["content"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    ids = [f"doc_{i}" for i in range(len(docs))]

    print("⏳ Embedding & upserting …")
    embeds = embedder.embed_documents(contents)
    collection.upsert(ids=ids, embeddings=embeds, metadatas=metadatas, documents=contents)
    print(f"✅ {len(docs)} documents indexés dans Chroma ({DATA_DIR})")

if __name__ == "__main__":
    build_index()
