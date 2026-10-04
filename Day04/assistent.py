from tool_manager import execute_tool

from openai import OpenAI
from dotenv import load_dotenv
import os

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
    tool_result = execute_tool(user_input)
    if tool_result:
        print(tool_result)
        continue
    message.append({"role": "user", "content": user_input})
    if user_input.lower() == 'exit':
        break
    response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
    message.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)


