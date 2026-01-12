import pandas as pd
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity
import joblib



def generate_embeddings(text):
    R= requests.post('http://localhost:11434/api/embed',
                     json={
                         'model' : 'bge-m3',
                         'input' :  text
                     })
    embedding = R.json()['embeddings']
    return embedding

    
df = joblib.load('chunks to embeddigs.joblib')



def inference(prompt):
    R = requests.post('http://localhost:11434/api/generate'
                      ,json=
                      {
                          'model': 'mistral:7b',
                          'prompt': prompt,
                          'stream' : False
                      })
    response = R.json()
    print(response['response'])
    return response['response']
    

userQuery = input('How may i help you?:')
user_embeddings = generate_embeddings([userQuery])[0]

#comparing Two vector embeddings from orginal embeddings and user input emdeddings using cosinesimilarity

similarities = cosine_similarity(np.vstack(df['embedding_label']),[user_embeddings]).flatten()
Top_embeddings = 3
index_limit = np.argsort(-similarities)[0:Top_embeddings]
print(index_limit)
newDf = df.loc[index_limit]
print(newDf[["Title",   "Start" , "End", "Text"]])


prompt = f'''  You are an expert teaching assistant for a React programming course.
You are given several video transcript chunks that include a "Title", "Start" time (in seconds), and "Text" content.

Your task:
- Answer the user's question **based only on the provided chunks**.
- Give the exact **start time** in (HH:MM:SS) format where the answer is found.
- Mention the **video title**.
- Add a short 1-2 sentence summary of what is taught there.
- If the question is **not related** to the video, respond with exactly:
  "Ask only relatable questions."

Now here are the video chunks:
{newDf[["Title",   "Start" , "End", "Text"]].to_json(orient="records")}

User question:
{userQuery}

Answer:




'''


#Prompt will save in Promt.txt which will handover to LLM to answer.
with open('prompt.txt', 'w') as f:
    f.write(prompt)

print("Waiting for response...")
responses = inference(prompt)


with open('Output.txt' , 'w') as f:
    f.write(responses)

print('Answer stored in Output.txt')    

