# app.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import subprocess

CHROMA_PATH = "chroma"
HF_CACHE = os.environ.get("HF_HOME", "/tmp/hf_cache")

# Ensure HF cache env is set before importing heavy libs (already set in Dockerfile/start script)
os.environ["HF_HOME"] = HF_CACHE

# If DB missing, create it
if not os.path.exists(CHROMA_PATH) or not any(os.scandir(CHROMA_PATH)):
    print("Chroma DB missing — building it now...")
    # Run your existing script to create DB
    subprocess.run(["python", "create_database.py"], check=True)

# Initialize embedding + DB once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# Small text generation model (CPU-friendly)
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=150,
    temperature=0.4,
)

app = FastAPI(title="RAG API")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/query")
def query_data(q: Query):
    query_text = q.question
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if not results or results[0][1] < 0.45:
        return {"response": "No good match found.", "sources": []}

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt = f"""Answer the question based only on the following context:\n\n{context_text}\n\nQuestion: {query_text}"""
    output = generator(prompt)[0]["generated_text"]
    sources = [doc.metadata.get("source", "unknown") for doc, _ in results]
    return {"response": output, "sources": sources}
