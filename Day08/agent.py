import asyncio

from openai import OpenAI
from dotenv import load_dotenv
from state import create_state, add_action, record_observation, next_step, can_continue, finish
import os


# load environment variables from .env file
load_dotenv()

# # Create an OpenAI client
openAiclient = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

from mcp_client import(connect, disconnect, discover_tools, execute_tool)


def build_tool_description(tools):
    descriptions = ""
    for tool in tools:
        descriptions += f"""
        Tool: {tool.name}
        Description: {tool.description}
        """
    return descriptions

def planner(user_request, tools):
    tool_descriptions = build_tool_description(tools)
    prompt = f"""
    You are AI Planner.
    Available tools: {tool_descriptions}
    Instruction: 
    1. Select the best tool
    2. Reply ONLY with the tool name
    3. Do not explain
    User request: {user_request}
    """
    response = openAiclient.chat.completions.create(model=os.getenv("MODEL"), messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()

def generate_response(user_request, tool_results):
    prompt = f"""
    The user request is: {user_request}
    The tool results are: {tool_results}
    Answer naturally.
    """
    response = openAiclient.chat.completions.create(model=os.getenv("MODEL"), messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()

async def main():
    client = await connect()
    tools = await discover_tools(client)
    user_request = input("Enter your request: ")
    tool_name = planner(user_request, tools)
    print("Selected tool:", tool_name)
    result = await execute_tool(client, tool_name)
    print(generate_response(user_request, result.content[0].text))
    await disconnect(client)

if __name__ == "__main__":
    asyncio.run(main())