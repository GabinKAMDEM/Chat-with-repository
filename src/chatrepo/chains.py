"""
Defines the QA pipeline and conversational chains for interacting with the indexed repository.
Includes memory persistence and prompt definitions.
"""
from typing import List, Tuple, Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, MessagesState

from .config import DATA_DIR, settings

# Initialize LLM for chat and QA
llm = ChatOpenAI(model=settings.llm_model,
                 api_key=settings.openai_api_key,
                 temperature=0)

# Setup embeddings and vector store for QA retrieval
embedder = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)
vectordb = Chroma(
    persist_directory=str(DATA_DIR),
    collection_name=settings.chroma_collection,
    embedding_function=embedder,
)
retriever = vectordb.as_retriever(search_kwargs={"k": 10})

# Prompt guiding the QA responses
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        You are an expert software assistant helping a developer understand a code repository.

        Use only the provided context to answer the question.
        If the answer is not contained in the context, say: "I couldn’t find this information in the repository."

        Give clear, concise, and technically accurate explanations. You may format code snippets using Markdown when needed.

        Context:
        ---------
        {context}
        ---------

        Question: {question}
        Answer:
        """.strip(),
)

class QAState(TypedDict):
    """State schema for QA pipeline."""
    question: str
    context: List
    answer: str
    #chat_history: List[Tuple[str, str]]

def retrieve(state: QAState) -> dict:
    """
    Retrieve top-k similar documents for the given question.
    """
    docs = vectordb.similarity_search(state["question"])
    return {"context": docs}

def generate(state: QAState) -> dict:
    """
    Generate an answer by formatting metadata and content, then invoking the LLM.
    """
    formatted_docs = []
    for doc in state["context"]:
        meta = "; ".join(f"{k}={v}" for k, v in doc.metadata.items())
        formatted_docs.append(f"[{meta}]\n{doc.page_content}")
    ctx = "\n\n---\n\n".join(formatted_docs)
    prompt_value = prompt.invoke({"context": ctx, "question": state["question"]})
    llm_response = llm.invoke(prompt_value)
    return {"answer": llm_response.content}

# Build and compile the QA graph with memory saver
qa_builder = StateGraph(QAState)
qa_builder.add_node(retrieve)
qa_builder.add_node(generate)
qa_builder.add_edge(START, "retrieve")
qa_builder.add_edge("retrieve", "generate")

memory = MemorySaver()
qa_graph = qa_builder.compile(checkpointer=memory)

def get_summary(thread_id : str | None = None) -> str:
    """
    Return a high-level summary of the repository (ignores chat history).
    """
    result = qa_graph.invoke({"question": """write a very detailed and professional presentation of this repository, 
                              allowing you to quickly get to grips with and launch the project. the project name should appear in the headline.
                              """},
                             config={"configurable": {"thread_id": thread_id}})
    return result["answer"]

def ask(question: str, thread_id : str | None = None, history: List[tuple[str, str]] | None = None) -> str:
    """
    Ask a question to the QA pipeline, with memory-based context.
    """
    if thread_id is None:
        thread_id = "nds154"
    result = qa_graph.invoke(
        {
            "question": question, 
        },
            config={"configurable": {"thread_id": thread_id}},
                             )
    return result["answer"]
