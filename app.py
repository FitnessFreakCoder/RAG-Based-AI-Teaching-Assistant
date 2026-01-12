from flask import Flask, render_template, request, jsonify, stream_with_context, Response
import numpy as np
import requests
import json
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
Api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Api_key) 

# Connect to your Chroma vector database
chroma_client = chromadb.PersistentClient(path="vector_db")
collection = chroma_client.get_or_create_collection(name="react_course")

# ---------- Embedding and model functions ---------- #

def generate_embeddings(text):
    """Generate embeddings using Ollama bge-m3 model"""
    try:
        R = requests.post('http://localhost:11434/api/embed', json={
            'model': 'bge-m3',
            'input': text
        })
        embedding = R.json()['embeddings']
        return embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None


def inference_stream(prompt):
    """Stream response from OpenAI GPT-4o-mini model"""
    try:
        stream = client.chat.completions.create(
            model="gpt-5.1",  # Using GPT-4o-mini (note: gpt-5-mini doesn't exist yet)
            messages=[
                {"role": "system", "content": "You are an expert teaching assistant for a React programming course."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"Error: {str(e)}"


def seconds_to_hms(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# ---------- Flask Routes ---------- #

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    """Handle user query and return streamed response"""
    user_query = request.json.get('query', '')

    if not user_query:
        return jsonify({'error': 'No query provided'}), 400

    # Generate embeddings for user query
    user_embeddings = generate_embeddings([user_query])
    if user_embeddings is None:
        return jsonify({'error': 'Failed to generate embeddings'}), 500

    user_embeddings = user_embeddings[0]

    # Query top 3 similar chunks from Chroma
    results = collection.query(
        query_embeddings=[user_embeddings],
        n_results=3
    )

    # Prepare context chunks for frontend
    context_chunks = []
    for i in range(len(results['documents'][0])):
        metadata = results['metadatas'][0][i]
        context_chunks.append({
            "Title": metadata.get("Title", "Unknown"),
            "Start_HMS": seconds_to_hms(metadata.get("Start", 0)),
            "End_HMS": seconds_to_hms(metadata.get("End", 0)),
            "Text": results['documents'][0][i]
        })

    # Create prompt for LLM
    prompt = f"""You are an expert teaching assistant for a React programming course.
You are given several video transcript chunks that include a "Title", "Start" time (in seconds), and "Text" content.

Your task:
- Answer the user's question **based only on the provided chunks**.
- Give the exact **start time** in (HH:MM:SS) format where the answer is found.
- Mention the **video title**.
- Add a short 1-2 sentence summary of what is taught there.
- If the question is **not related** to the video, respond with exactly:
  "Ask only relatable questions."

Now here are the video chunks:
{json.dumps(context_chunks, indent=2)}

User question:
{user_query}

Answer:
"""

    # Stream data back to client
    def generate():
        # Send context first
        yield f"data: {json.dumps({'type': 'context', 'chunks': context_chunks})}\n\n"

        # Stream model output
        for chunk in inference_stream(prompt):
            yield f"data: {json.dumps({'type': 'response', 'text': chunk})}\n\n"

        # Signal completion
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        R = requests.get('http://localhost:11434/api/tags', timeout=5)
        ollama_status = "connected" if R.status_code == 200 else "disconnected"
    except:
        ollama_status = "disconnected"

    # Also verify Chroma connection
    try:
        collections = chroma_client.list_collections()
        chroma_status = "connected" if len(collections) > 0 else "empty"
    except Exception as e:
        chroma_status = f"error: {e}"

    # Check OpenAI connection
    try:
        client.models.list()
        openai_status = "connected"
    except:
        openai_status = "disconnected"

    return jsonify({
        'status': 'running',
        'ollama': ollama_status,
        'openai': openai_status,
        'chroma': chroma_status
    })


if __name__ == '__main__':
    print("✅ Connected to ChromaDB at ./vector_db")
    print("Starting Flask server on http://localhost:5000 ...")
    app.run(debug=True, port=5000, threaded=True)