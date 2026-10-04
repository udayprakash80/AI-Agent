from tool_manager import execute_tool
from tools import read_text_file
from planner import choose_tool

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

print("=" * 60)
print("Hello, I am your AI assistant. How can I help you today?")
print("=" * 60)

message = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ")
    text = user_input.lower()
    if text.startswith("summarize"):
        filename = user_input[10:].strip()
        file_content = read_text_file("data/" + filename)
        prompt = f"""
        Summarize the following document.
        Document: 
        {file_content} 
        """
        message.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
        print(response.choices[0].message.content)
        continue
    if text.startswith("explain"):
        filename = user_input[8:].strip()
        file_content = read_text_file("data/" + filename)
        prompt = f"""
        Explain the following document.
        Document: 
        {file_content} 
        """
        message.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
        print(response.choices[0].message.content)
        continue
    if text.startswith("ask"):
        parts = user_input.split(maxsplit=2)
        filename = parts[1].strip()
        question = parts[2].strip()
        file_content = read_text_file("data/" + filename)
        prompt = f"""
        You are given a document.
        
        Answer the user's question using only the information present in the document.
        
        If the answer is not in the document, say "I couldn't find that information in the document."
        Document: 
        {file_content} 
        Question: 
        {question}
        """
        message.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
        print(response.choices[0].message.content)
        continue
    tool_result = choose_tool(user_input)
    if tool_result != "none":
        print(execute_tool(tool_result))
        continue
    message.append({"role": "user", "content": user_input})
    if user_input.lower() == 'exit':
        break
    response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
    # message.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)


