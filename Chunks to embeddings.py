import os
import json
import requests
import chromadb
import pandas as pd

# Create or connect to a Chroma database folder
chroma_client = chromadb.PersistentClient(path="vector_db")

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="react_course")

def generate_embeddings(texts):
    """Generate embeddings using Ollama (bge-m3 model)."""
    R = requests.post('http://localhost:11434/api/embed', json={
        'model': 'bge-m3',
        'input': texts
    })
    embeddings = R.json()
    return embeddings['embeddings']


# Load all JSON chunks
json_files = os.listdir('Jsons')
chunk_label = 0

for file in json_files:
    with open(f'Jsons/{file}', 'r') as f:
        data = json.load(f)

    print(f"Creating embeddings for {file}")
    texts = [c['Text'] for c in data['chunks']]
    embeddings = generate_embeddings(texts)

    # Store chunks in Chroma
    for i, chunk in enumerate(data['chunks']):
        chunk_id = f"{file}_{i}"
        metadata = {
            "Title": chunk.get("Title"),
            "Start": chunk.get("Start"),
            "End": chunk.get("End"),
            "File": file
        }

        collection.add(
            ids=[chunk_id],
            embeddings=[embeddings[i]],
            documents=[chunk['Text']],
            metadatas=[metadata]
        )
        chunk_label += 1

print("✅ All embeddings stored in Chroma vector database at ./vector_db")
