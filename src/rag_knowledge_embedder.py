import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load Excel file
df = pd.read_excel("Assignment Data Base.xlsx")
sentences = df.iloc[:, 1].dropna().astype(str).tolist()

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(sentences)

# Build FAISS index
embedding_matrix = np.array(embeddings).astype("float32")
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)
faiss.write_index(index, "kb.index")

# Save original sentences
with open("kb_sentences.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sentences))

print("Knowledge base indexed using sentence-transformers.")