from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_cree_documents(docs: List[Dict], chunk_size=500, chunk_overlap=100) -> List[Dict]:
    """
You are a project assistant with access to Jira and Confluence data.

Your job is to respond clearly using only the provided context. Do not guess.

If the user asks about a specific Jira ID (like 10003), look for exact matches.

Context:
{context}

Question:
{question}

Answer in detail:
"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = []

    for doc in docs:
        # Combine the title and main content (can be from description, etc.)
        full_text = f"{doc.get('title', '')}\n{doc.get('description', '')}"

        split_texts = splitter.split_text(full_text)

        for i, chunk_text in enumerate(split_texts):
            chunk = {
                "chunk_id": f"{doc['source']}_{doc['title'][:30].replace(' ', '_')}_{i}",
                "source": doc["source"],
                "title": doc["title"],
                "text": chunk_text
            }

            # Copy over all other fields from the original doc
            for key, value in doc.items():
                if key not in chunk:
                    chunk[key] = value

            chunks.append(chunk)

    return chunks