from flask import Flask, render_template, request, redirect, url_for
from sentence_transformers import SentenceTransformer, util
import numpy as np
import ollama, pprint, os

def load_text_from_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file
            data = file.read()
            return data
    else:
        return None

# Cortamos el menú por secciones (cada bloque "== TÍTULO ==" con sus líneas)
def trocear(texto):
    chunks, actual = [], []
    for linea in texto.split("\n"):
        if linea.startswith("== ") and linea.endswith(" =="):
            if actual: chunks.append("\n".join(actual).strip())
            actual = [linea]
        else:
            actual.append(linea)
    if actual: chunks.append("\n".join(actual).strip())
    return [c for c in chunks if c]

# Define the path to the text file
file_path = 'Dieta/Semana1-2.txt'
# Load the content from the file into the DATA variable
DATA = load_text_from_file(file_path)
secciones = trocear(DATA)

# Modelo de embeddings MULTILINGÜE (entiende español)
buscador = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

emb_secciones = buscador.encode(secciones, convert_to_tensor=True)

def buscar(pregunta, k=3):
    """Regresa las k secciones del menú más parecidas a la pregunta."""
    emb_q = buscador.encode(pregunta, convert_to_tensor=True)
    hits = util.semantic_search(emb_q, emb_secciones, top_k=k)[0]
    return [secciones[h["corpus_id"]] for h in hits]

app = Flask(__name__)

# Replace 'localhost:12345' with the actual address of your Ollama server
ollama_server = 'localhost:11434'
#model = "llama3.1:8b"
model = "llama3.2:3b"
history = []

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/get')
def get_ia_response():
    #question = request.form['question']
    userText = request.args.get('msg')  
    fragmento = buscar(userText)
    prompt_rag = f"""Responde la pregunta del usuario usando la siguiente politica. Si la politica no cubre la pregunta, dilo claramente y despues ofrece una respuesta adicional fuera de la politica, pero indica  que esa respuesta esta fuera de la politica.

Política: {fragmento}

Pregunta: {userText}

Responde con tono alegre y positivo asi como motivador. Respuesta corta y breve."""


    message = {
        "role": "user", 
        "content": prompt_rag
    }
    history.append(message)
    response =  ollama.chat(model=model, messages=history)
    pprint.pp(response)
    answer = response.message.content
    return answer

if __name__ == '__main__':
    app.run(debug=True)

