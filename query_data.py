import argparse
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import os

os.environ["HF_HOME"] = r"D:\huggingface_cache"

CHROMA_PATH = "chroma"

# 1️⃣ Text generation model
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=150,  # generate up to 150 tokens
    temperature=0.5,
    pad_token_id=50256   # avoid warnings about EOS token
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # 2️⃣ Chroma DB + embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # 3️⃣ Search
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.5:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    # 4️⃣ Prepare prompt
    prompt = f"""
Answer the question based only on the following context:

{context_text}

Question: {query_text}
"""

    # 5️⃣ Generate response
    response_text = generator(prompt)[0]['generated_text']

    sources = [doc.metadata.get("source", None) for doc, _ in results]
    print(f"Response: {response_text}\nSources: {sources}")

if __name__ == "__main__":
    main()
