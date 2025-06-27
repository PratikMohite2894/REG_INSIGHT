import os
import json
from typing import List
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

def load_chunks(path: str) -> List[Document]:
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    documents = []
    for chunk in chunks:
        metadata = {
            "source": chunk["source"],
            "title": chunk["title"],
            "chunk_id": chunk["chunk_id"]
        }
        documents.append(Document(page_content=chunk["text"], metadata=metadata))

    return documents

def embed_chunks_and_save(chunks_path="backend/data/chunks.json", db_path="backend/vectore/"):
    print("📦 Loading chunks...")
    documents = load_chunks(chunks_path)
    

    print(f"✨ Generating embeddings for {len(documents)} chunks...")
    # embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    db = FAISS.from_documents(documents, embedding_model)
    
    print("💾 Saving vector store to disk...")
    db.save_local(db_path)
    print(f"✅ FAISS vector store saved at: {db_path}")

if __name__ == "__main__":
    embed_chunks_and_save()