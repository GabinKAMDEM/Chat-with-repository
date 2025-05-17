import streamlit as st
from chatrepo import api

st.set_page_config(page_title="Chat-with-Repo", page_icon=":robot_face:")
st.title("🚀 Chat-with-Repository")

tab1, tab2 = st.tabs(["Résumé", "Chat"])

with tab1:
    with st.spinner("Ingestion & indexation en cours…"):
        from chatrepo.index import build_index
        build_index()
        st.success("Index prêt !")
        st.markdown(api.get_summary())

with tab2:
    if "history" not in st.session_state:
        st.session_state["history"] = []

    for role, msg in st.session_state["history"]:
        st.chat_message(role).write(msg)

    prompt = st.chat_input("Pose ta question…")
    if prompt:
        st.session_state["history"].append(("user", prompt))
        with st.spinner("✍️"):
            answer = api.ask(prompt, st.session_state["history"])
        st.session_state["history"].append(("assistant", answer))
        st.chat_message("assistant").write(answer)
