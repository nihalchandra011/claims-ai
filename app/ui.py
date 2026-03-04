import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.parsers import parse_any
from backend.agent import agent_answer

st.title("ClaimsAI")
st.subheader("Expert Claims & Contract Mentor")

uploaded_file = st.file_uploader(
    "Upload a claim or contract file (optional)",
    type=["txt","dat","pdf","csv","xlsx","docx","png","jpg","jpeg"]
)

parsed_metadata = {}

if uploaded_file:

    file_bytes = uploaded_file.read()

    parsed_metadata = parse_any(file_bytes, uploaded_file.name)

    st.success("File processed")

    st.json(parsed_metadata)


st.divider()

user_question = st.text_input("Ask ClaimsAI anything")

if user_question:

    placeholder = st.empty()

    with st.spinner("Thinking..."):

        answer = agent_answer(parsed_metadata or {}, user_question)

    placeholder.markdown(answer)