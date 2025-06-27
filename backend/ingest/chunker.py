from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs: List[Dict], chunk_size=500, chunk_overlap=100) -> List[Dict]:
    """
    Splits documents into smaller chunks for embedding and retrieval.

    Args:
        docs (List[Dict]): A list of documents with 'title' and 'content'.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlap between chunks.

    Returns:
        List[Dict]: A list of chunks with metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = []

    for doc in docs:
        full_text = f"{doc['title']}\n{doc['content']}"
        split_texts = splitter.split_text(full_text)

        for i, chunk_text in enumerate(split_texts):
            chunks.append({
                "chunk_id": f"{doc['source']}_{doc['title'][:30].replace(' ', '_')}_{i}",
                "source": doc['source'],
                "title": doc['title'],
                "text": chunk_text
            })

    return chunks