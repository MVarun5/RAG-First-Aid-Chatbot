import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="💬")
st.title("🩺 RAG-Powered First-Aid Chatbot for Diabetes, Cardiac & Renal Emergencies")

query = st.text_input("Ask your question about diabetes, cardiac, or renal emergencies:")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={"query": query}
                )
                result = response.json()
                st.success("Answer:")
                disclaimer = result.get("disclaimer", "⚠️ “This information is for educational purposes only and is not a substitute for professional medical advice.”")
                st.markdown(disclaimer)
                st.markdown(result.get("response", " No answer returned."))
            except Exception as e:
                st.error(f"Something went wrong: {e}")
