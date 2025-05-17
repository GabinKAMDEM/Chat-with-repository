from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

from .config import DATA_DIR, settings

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

def get_retriever():
    embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)

    vectordb = Chroma(
        persist_directory=str(DATA_DIR),
        collection_name=settings.chroma_collection,
        embedding_function=embeddings,  
    )
    return vectordb.as_retriever(search_kwargs={"k": 5})

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=get_retriever(),
    return_source_documents=True,
)

summary_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=get_retriever(),
)

def get_summary() -> str:
    return summary_chain.invoke(
        {"query": "Give me an executive summary of the repository."}
    )["result"]

def ask(question: str, history: list[tuple[str, str]] | None = None) -> str:
    history = history or []
    out = qa_chain.invoke({"question": question, "chat_history": history})
    return out["answer"]