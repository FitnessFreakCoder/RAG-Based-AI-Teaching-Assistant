<img width="1889" height="1020" alt="Screenshot 2026-01-12 153419" src="https://github.com/user-attachments/assets/7ff59b67-446d-4ef8-ac14-a7dd2c7e6d4a" />
<img width="1896" height="1031" alt="Screenshot 2026-01-12 153409" src="https://github.com/user-attachments/assets/da729801-218c-4c30-9bb2-df5d63747395" />
# 🧠 RAG-Based AI Teaching Assistant

An intelligent Retrieval-Augmented Generation (RAG) system that allows users to ask natural language questions over large collections of documents and video transcripts, delivering accurate, context-aware answers using embeddings, vector databases, and Large Language Models.

This project is built to demonstrate how modern AI assistants like ChatGPT can be customized to work on private knowledge sources such as YouTube videos, PDFs, notes, and course material.

---

Note: I have done process for 1video from youtube.
video length: 8hrs+

## 🚀 What This Project Does

Instead of relying on the LLM’s built-in knowledge, this system:

1. Converts documents and video transcripts into vector embeddings  
2. Stores them inside a vector database  
3. Retrieves only the most relevant chunks when a user asks a question  
4. Sends those chunks to an LLM to generate grounded, factual answers  

This eliminates hallucinations and makes the AI answer strictly from your own data.

---

## 🧩 System Architecture
User Question
↓
Embedding Model
↓
Vector Database (Chroma / FAISS)
↓
Top-K Relevant Chunks
↓
LLM (GPT / Llama / Mistral)
↓
Final Answer



---

## 🛠️ Tech Stack

- **LLM** – OpenAI / LLaMA / Mistral
- **Embeddings** – OpenAI Embeddings / SentenceTransformers
- **Vector Database** – ChromaDB / FAISS
- **Backend** – Python
- **Data Sources** – YouTube transcripts, PDFs, text documents
- **APIs** – Speech-to-Text, Text-to-Speech (optional)

---

## 📂 Project Workflow

1. **Data Collection**
   - Extract transcripts from YouTube videos or documents

2. **Chunking**
   - Split text into small overlapping chunks for better retrieval

3. **Embedding**
   - Convert each chunk into a vector using an embedding model

4. **Storage**
   - Store embeddings in a vector database

5. **Querying**
   - User query is converted into an embedding
   - Nearest chunks are retrieved from the vector DB

6. **Answer Generation**
   - Retrieved context is injected into the LLM prompt
   - Model generates a grounded response

---

## 💡 Why RAG is Better Than Normal Chatbots

| Normal LLM | RAG-Based System |
|-----------|----------------|
| Hallucinates answers | Uses real data |
| Cannot read private files | Works on your documents |
| Fixed knowledge | Fully customizable |
| No citations | Context-aware answers |

---

## 📌 Example Use Cases

- AI Tutor for courses
- YouTube video question answering
- Company knowledge base chatbot
- Research assistant
- Legal & policy document QA

---

## 🧪 Sample Query

What are props in React?
📚 Relevant Video Sections
Complete React course with projects
01:59:16 - 01:59:36
We have to give props to react element React Elements Dot props Ok So here it has an issue And it has been solved here But there is still a bug, let's solve it And The next thing we have is
Complete React course with projects
03:39:52 - 03:40:12
whenever I declare this function I get access to props by default it is called props I am not saying react calls it props if I wanted I would have said properties Hitesh would have said, why properties but ok, you get these values but it has one more syntax you should know original syntax
Complete React course with projects
00:21:06 - 00:21:26
Yes, it is It is called props It is properties That's why I say As much as you understand It will be easy This is reusing After that How to propagate I told you
💡 Answer
- **Answer from the video:**  
  In React, *props* are the *properties* you pass into components; they are the values/data given to a React element or component so it can receive and use information from its parent.

- **Where this is taught:**
  - **Title:** Complete React course with projects  
    **Start time:** 00:21:06  
    **Summary:** The instructor explains that “props” stands for “properties” in React and are used to reuse components and propagate data to them.
  - **Title:** Complete React course with projects  
    **Start time:** 03:39:52  
    **Summary:** The instructor shows that when you declare a component function you get a `props` parameter (you could name it something else like `properties`), and it contains the values passed into that component.

---

## 🔧 How to Run

bash
pip install -r requirements.txt
python ingest.py     # create embeddings
python app.py        # start assistant


