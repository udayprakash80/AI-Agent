from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def create_embedding(text):
    response = client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )
    return response.data[0].embedding
