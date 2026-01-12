import whisper
import torch
import warnings
import json
import os


# Suppress warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Setup GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using: {device}")

#load model
model = whisper.load_model("large-v2", device=device)

# Combined Chunk

def combineded_chunks(chunks, chunkpergroup=10):
    combined_chunks = []
    current_chunk = []
    for i, chunk in enumerate(chunks):
        current_chunk.append(chunk)

        if len(current_chunk) == chunkpergroup or i == len(chunks) - 1:
            combined = {
                "Title": current_chunk[0]['Title'],
                "Start": current_chunk[0]['Start'],
                "End": current_chunk[-1]['End'],
                "Text": " ".join([c['Text'] for c in current_chunk])
            }
            combined_chunks.append(combined)
            current_chunk = []
    return combined_chunks        

audiofile = "Sample Mp3 Audio.mp3"
title = audiofile.split('.')[0]
# Create output directory if it doesn't exist

if not os.path.exists(f"audios/{audiofile}"):
    print('Audiofile not found!!')
    for file in os.listdir('audios'):
        if file.endswith('.mp3'):
            print(f'Creating audiofile directory.... {title} ')
    

else:
    print(f'Processing audiofile....{title}')
    result = model.transcribe(f'audios/{audiofile}', 
                              language="hi",
                              task="translate",
                              word_timestamps=False,
                              verbose=True,)
    chunks=[]
    for segment in result['segments']:
        chunks.append({
            "Title" : title,
            "Start" : segment['start'],
            "End" : segment['end'],
            "Text" : segment['text']
        })  

    combined_chunks = combineded_chunks(chunks, chunkpergroup=10)

    chunkswithmedadata = {
        "chunks": combined_chunks,
        "text": result["text"],
        "original_chunk_count": len(chunks),
        "combined_chunk_count": len(combined_chunks)
    }

    os.makedirs("Jsons", exist_ok=True)

    Outputfile = f'Jsons/{title}.json'
    with open(Outputfile, 'w', encoding='utf-8') as f:
        json.dump(chunkswithmedadata, f,  indent=4)