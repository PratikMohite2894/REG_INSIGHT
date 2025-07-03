from .loader import combine_data
from .chunker import chunk_documents
import json
from .CreeLoader import combine_cree_data
from .CreeChuncker import chunk_cree_documents

# Load your data
docs = combine_data("backend/data/all_jira_issues.json", "backend/data/all_confluence_pages.json")

# Chunk the documents
chunks = chunk_documents(docs)

# Print summary
print(f"✅ Total Chunks for Sierra: {len(chunks)}")
print("🔍 Sample Chunk:\n", chunks[0])


# Save to chunks.json
with open("backend/data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)