from openai import OpenAI
from dotenv import load_dotenv
import os
from retriever import retrieve
from pathlib import Path


def load_documents():
    documents = {}
    for file in Path("knowledge").glob("*.txt"):
        documents[file.name] = file.read_text(
            encoding="utf-8"
        )
    return documents

documents = load_documents()


load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

roleList = [{"key": "1", "content": "You are a python teacher"},
            {"key": "2", "content": "You are a tour guide"},
            {"key": "3", "content": "You are a math teacher"}]

print("Enter your type of assistant:")
print("1. Python teacher")
print("2. Tour guide")
print("3. Math teacher")
input_key = input("Enter your choice: ")
if(input_key not in ["1", "2", "3"]):
    raise Exception(
        "Invalid input. Please enter a number between 1 and 3."
    )

print("=" * 60)
print("Hello, I am your AI assistant. How can I help you today?")
print("=" * 60)

message = [
    {"role": "system", "content": roleList[int(input_key) - 1]["content"]}
]

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ")
    message.append({"role": "user", "content": user_input})
    if user_input.lower() == 'exit':
        break
    best_match = retrieve(user_input, documents)
    print(best_match)
    message.append({"role": "system", "content": "Answer only from the provided context"})
    prompt = f"""
    Answer the user's question based on the following information.
    Context: {best_match['content']}
    Question: {user_input}
    If the answer is not in the context, say "I couldn't find that information in the document."
    """
    message.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
    message.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)