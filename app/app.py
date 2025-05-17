import streamlit as st
from chatrepo import api

st.set_page_config(page_title="Chat-with-Repo", page_icon=":robot_face:")
st.title("🚀 Chat-with-Repository")

repo_url = st.sidebar.text_input(
    "Git repository URL",
    value="https://github.com/...",
    placeholder="https://github.com/user/project",
    key="repo_url",
)

if st.sidebar.button("Index & start chat", key="btn_index"):
    with st.spinner("Cloning, parsing, embedding …"):
        api.build_index(repo_url)
        st.session_state["index_ready"] = True
        st.session_state["repo_summary"] = api.get_summary()
        st.sidebar.success("")

ready = st.session_state.get("index_ready", False)
tab1, tab2 = st.tabs(["Summary", "Chat"])

with tab1:
    if ready:
        st.markdown(st.session_state["repo_summary"])
    else:
        st.info("➡️ Enter a repo URL in the sidebar and click *Start chat*.")

with tab2:
    if not ready:
        st.info("Chat disabled until the index is built.")
    else:
        history = st.session_state.setdefault("history", [])

        for role, msg in history:
            st.chat_message(role).write(msg)

        if prompt := st.chat_input("Ask a question …"):
            history.append(("user", prompt))
            with st.spinner("🧠 Thinking…"):
                answer = api.ask(prompt, history)
            history.append(("assistant", answer))
            st.chat_message("assistant").write(answer)
