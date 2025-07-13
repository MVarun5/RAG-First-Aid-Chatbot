from flask import Flask, request, jsonify
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

app = Flask(__name__)

# Load API keys from environment (recommended)
SERPER_API_KEY = os.getenv("SERPER_API_KEY") or "16946a0523aaab14dc13c1f92f667fe0271e25a8"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

# Load FAISS index and KB sentences
index = faiss.read_index("kb.index")
with open("knowledgebase_sentences.txt", "r", encoding="utf-8") as f:
    sentences = f.readlines()

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Claude via OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Search top-k relevant lines from local KB
def search_kb(query, top_k=3):
    query_emb = embedder.encode([query]).astype("float32")
    D, I = index.search(query_emb, top_k)
    return [sentences[i].strip() for i in I[0]]

# Fetch top web results using Serper.dev
def search_web(query):
    headers = {"X-API-KEY": SERPER_API_KEY}
    data = {"q": query}
    res = requests.post("https://google.serper.dev/search", json=data, headers=headers)
    results = res.json().get("organic", [])
    return "\n\n".join(f"{r['title']}\n{r['snippet']}\n{r['link']}" for r in results[:3])

# Combine everything into a prompt for Claude
def build_prompt(user_input):
    local = search_kb(user_input)
    web = search_web(user_input)
    return f"""You are a helpful AI assistant specialized in first-aid for diabetes, cardiac, and renal emergencies.

User Question:
{user_input}

Local Knowledge:
{chr(10).join(local)}

Web Results:
{web}

Answer with clarity and safety. Always end with this disclaimer:
🩺 This is not medical advice. For emergencies, contact a healthcare professional.
"""

# Call Claude via OpenRouter API
def query_claude(prompt):
    response = client.chat.completions.create(
        model="anthropic/claude-3-sonnet:beta",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET"])
def home():
    return "✅ Claude RAG Chatbot API is running!"

# Flask endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("query", "")
    if not user_input:
        return jsonify({"error": "Query is missing"}), 400
    prompt = build_prompt(user_input)
    try:
        response = query_claude(prompt)
        return jsonify({
            "response": response,
            "disclaimer": "⚠️ “This information is for educational purposes only and is not a substitute for professional medical advice.” "
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(debug=True)
