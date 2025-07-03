from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_cree_documents(docs: List[Dict], chunk_size=500, chunk_overlap=100) -> List[Dict]:
    """
    Splits CREE documents (Jira + Confluence) into smaller chunks for embedding and retrieval.

    Args:
        docs (List[Dict]): List of documents with metadata.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlap between chunks to preserve context.

    Returns:
        List[Dict]: List of chunked documents with full metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = []

    for doc in docs:
        # 👇 Dynamically combine all key-value pairs (excluding source and chunk_id)
        full_text_parts = []
        for key, value in doc.items():
            if key not in {"chunk_id", "text"}:
                if isinstance(value, list):
                    value = ", ".join(value)
                full_text_parts.append(f"{key.capitalize().replace('_', ' ')}: {value}")
        full_text = "\n".join(full_text_parts)

        # 🔁 Split the full_text
        split_texts = splitter.split_text(full_text)

        for i, chunk_text in enumerate(split_texts):
            chunk = {
                "chunk_id": f"{doc['source']}_{doc.get('jira_id', doc.get('confluence_id', ''))}_{i}",
                "source": doc["source"],
                "title": doc.get("title", ""),
                "text": chunk_text
            }

            # 🧾 Add full original metadata to each chunk
            for key, value in doc.items():
                if key not in chunk:
                    chunk[key] = value

            chunks.append(chunk)

    return chunks
