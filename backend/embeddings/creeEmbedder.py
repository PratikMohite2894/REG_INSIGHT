# File: backend/ingest/cree_embedder.py

import os
import json
from typing import List
from dotenv import load_dotenv
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
            "source": chunk.get("source"),
            "title": chunk.get("title"),
            "chunk_id": chunk.get("chunk_id"),
            "jira_id": chunk.get("jira_id", ""),
            "description": chunk.get("description", ""),
            "created_date": chunk.get("created_date", ""),
            "updated_date": chunk.get("updated_date", ""),
            "status": chunk.get("status", ""),
            "assignee": chunk.get("assignee", ""),
            "reporter": chunk.get("reporter", ""),
            "priority": chunk.get("priority", ""),
            "eta": chunk.get("eta", ""),
            "created_by": chunk.get("created_by", ""),
            "acceptance_criteria": chunk.get("acceptance_criteria", "")
        }
        documents.append(Document(page_content=chunk["text"], metadata=metadata))

    return documents

def embed_chunks_and_save(chunks_path="C:/Users/PratikMohite/OneDrive - Atyeti Inc/Desktop\project-genius/backend/data/creeData/cree_chuncks.json", db_path="cree_vectore/"):
    print("📦 Loading CREE chunks...")
    documents = load_chunks(chunks_path)

    print(f"✨ Generating embeddings for {len(documents)} CREE chunks...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(documents, embedding_model)

    print("💾 Saving CREE vector store to disk...")
    db.save_local(db_path)
    print(f"✅ FAISS vector store saved at: {db_path}")

if __name__ == "__main__":
    embed_chunks_and_save()
