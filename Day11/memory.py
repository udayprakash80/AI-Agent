import json
import sqlite3
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

import os
load_dotenv()

DATABASE="memory.db"
openAiclient = OpenAI(base_url=os.getenv('BASE_URL'), api_key=os.getenv('API_KEY'))

def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    assistant_message TEXT,
    embedding_json TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
    connection.commit()
    connection.close()

def create_embedding(text):
    response = openAiclient.embeddings.create(model="text-embedding-3-small",input=text)
    return response.data[0].embedding

def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def save_memory(user_message, assistant_message):
    text = user_message + "\n" + assistant_message
    embedding = create_embedding(text)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO memories (user_message, assistant_message, embedding_json) VALUES (?, ?, ?)""", (user_message, assistant_message, json.dumps(embedding)))
    connection.commit()
    connection.close()

def search_semantic_memories(query, top_k=3, threshold=0.60):
    query_embedding = create_embedding(query)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT user_message, assistant_message, embedding_json, created_at FROM memories""")
    rows = cursor.fetchall()
    connection.close()
    results = []
    for(user_message, assistant_message, embedding_json, created_at) in rows:
        memory_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, memory_embedding)
        if(score >= threshold):
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "score": score ,
                "created_at": created_at
            })
            results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]