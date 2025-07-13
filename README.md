# RAG-Powered First-Aid Chatbot

## Overview
A RAG (Retrieval-Augmented Generation) powered chatbot specialized in providing first-aid guidance for diabetes, cardiac, and renal emergencies. The system combines local knowledge base search with real-time web search to provide comprehensive and up-to-date medical information.

🚨 IMPORTANT DISCLAIMER
This chatbot is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. In case of medical emergencies, always contact emergency services or healthcare professionals immediately.

## Features

Hybrid Knowledge Retrieval: Combines local medical knowledge base with real-time web search
Specialized Domain: Focused on diabetes, cardiac, and renal emergency first-aid
Multiple Interfaces: Both Flask web API and command-line interface
Semantic Search: Uses sentence transformers for intelligent knowledge retrieval
AI-Powered Responses: Leverages Claude 3 Sonnet for natural language generation
Safety First: All responses include medical disclaimers

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/MVarun5/RAG-First-Aid-Chatbot.git
   cd RAG-First-Aid-Chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   - `SERPER_API_KEY`: Get from [Serper.dev](https://serper.dev/).
   - `OPENROUTER_API_KEY`: Get from [OpenRouter](https://openrouter.ai/).
   ```bash
   export SERPER_API_KEY="your_key"
   export OPENROUTER_API_KEY="your_key"
   ```
4. Embed knowledge base:
   ```bash
   python src/rag_knowledge_embedder.py
   ```
5. Run the Flask API:
   ```bash
   python src/rag_api.py
   ```
6. Run the Streamlit UI:
   ```bash
   streamlit run src/rag_streamlit_ui.py
   ```

## Usage
- Access the UI at `http://localhost:8501`.
- Enter a query (e.g., "Shaky and glucose 55 mg/dL") and click "Ask".
- Use the CLI by running `python src/rag_cli_interface.py` and typing queries.

## Design Trade-Offs
- **Local vs. Web Search**: Local FAISS search is fast but limited; web search adds relevance but increases latency.
- **API Dependency**: External APIs (Serper, OpenRouter) enhance accuracy but risk downtime.
- **Response Length**: Capped at 250 words for clarity, trading off detailed explanations.
