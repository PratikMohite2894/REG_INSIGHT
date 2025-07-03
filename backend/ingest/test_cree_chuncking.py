# from .CreeLoader import combine_cree_data
# from .CreeChuncker import chunk_cree_documents
from ingest.CreeChuncker import chunk_cree_documents
import json
from ingest.CreeLoader import combine_cree_data

docs_cree = combine_cree_data("C:/Users/PratikMohite/OneDrive - Atyeti Inc/Desktop/project-genius/backend/data/creeData/all_cree_jira.json",
    "C:/Users/PratikMohite/OneDrive - Atyeti Inc/Desktop/project-genius/backend/data/creeData/all_cree_confluence.json")
# Chunk the documents
chunks = chunk_cree_documents(docs_cree)
# Print summary

print(f"✅ Total Chunks for cree : {len(chunks)}")
print("🔍 Sample Chunk:\n", chunks[0])


# Save to chunks.json
with open("C:/Users/PratikMohite/OneDrive - Atyeti Inc/Desktop/project-genius/backend/data/creeData/cree_chuncks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)