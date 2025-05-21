"""
Streamlit application to index a GitHub repository and interact via chat.
- Clone and embed repository content.
- Display repository summary and modules.
- Provide a chat interface using the built index.
"""
import streamlit as st
from chatrepo import api
import uuid


st.set_page_config(page_title="Chat‑with‑Repo", page_icon="📝", layout="wide")

st.title("🚀 Chat‑with‑Repository")

repo_url = st.sidebar.text_input(
    "Git repository URL", value="https://github.com/", placeholder="https://github.com/user/project"
)
if st.sidebar.button("Index & start chat"):
    with st.spinner("Cloning, parsing, embedding …"):
        api.build_index(repo_url)
        st.session_state.index_ready = True
        if "session_id" not in st.session_state:
            st.session_state["session_id"] = str(uuid.uuid4())
        st.session_state.repo_summary = api.get_summary(thread_id=st.session_state["session_id"])
        st.sidebar.success("Index ready !")

ready = st.session_state.get("index_ready", False)

summary_tab, modules_tab, chat_tab = st.tabs(["Summary", "Modules", "Chat"])

with summary_tab:
    if ready:
        st.markdown(st.session_state.repo_summary)
    else:
        st.info("➡️ Enter a repo URL in the sidebar and click *Index & start chat*.")

with modules_tab:
    if not ready:
        st.info("Index the repo first")
    else:
        module = st.selectbox("Module", api.list_modules())  
        if module:
            symbols = api.list_symbols(module)
            
            names = [f"{s['kind']} → {s['name']}" for s in symbols]
            idx = st.radio("Symbols", names, index=0, key="sym_radio")
            sym = symbols[names.index(idx)]
            st.code(sym["signature"], language="python")
            st.markdown(sym.get("docstring") or "*no docstring*")

with chat_tab:
    if not ready:
        st.info("Chat disabled until the index is built.")
    else:
        if "history" not in st.session_state:
            st.session_state["history"] = []  
        for role, msg in st.session_state["history"]:
            st.chat_message(role).write(msg)

        question = st.chat_input("Ask a question …")
        if question:
            st.session_state["history"].append(("user", question))
            st.chat_message("user").write(question)

            with st.spinner("Thinking…"):
                answer = api.ask(question = question,
                                 history=st.session_state["history"],
                                 thread_id=st.session_state["session_id"])

            st.session_state["history"].append(("assistant", answer))
            st.chat_message("assistant").write(answer)
