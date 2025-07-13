import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

# Load API Keys securely - FIXED
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load FAISS index and sentences
index = faiss.read_index("kb.index")
with open("kb_sentences.txt", "r", encoding="utf-8") as f:
    sentences = f.readlines()

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Local KB search
def search_kb(query, top_k=3):
    query_emb = embedder.encode([query]).astype("float32")
    D, I = index.search(query_emb, top_k)
    return [sentences[i].strip() for i in I[0]]

# Web search using Serper.dev
def search_web(query):
    headers = {"X-API-KEY": SERPER_API_KEY}
    data = {"q": query}
    res = requests.post("https://google.serper.dev/search", json=data, headers=headers)
    results = res.json().get("organic", [])
    return "\n\n".join(f"{r['title']}\n{r['snippet']}\n{r['link']}" for r in results[:3])

# Build Claude-compatible prompt
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

Answer with clarity and safety. Always add this disclaimer: 
This is not medical advice. For emergencies, contact a healthcare professional.
"""

# Set up Claude via OpenRouter - FIXED
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY  # Use the variable directly
)

# Call Claude via OpenRouter
def query_claude(prompt):
    response = client.chat.completions.create(
        model="anthropic/claude-3-sonnet:beta",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

# CLI Chatbot
if __name__ == "__main__":
    print(" Claude-Powered First-Aid Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        prompt = build_prompt(user_input)
        answer = query_claude(prompt)
        print("\nBot:", answer, "\n")