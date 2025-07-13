import streamlit as st

def test_ui_input():
    st.text_input = lambda x: "Test query"
    assert st.text_input("Ask your question") == "Test query"