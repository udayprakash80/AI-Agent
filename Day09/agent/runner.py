from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

from planner import planner
from executer import execute_action
from loop import run_agent_loop
from mcp_client import*

load_dotenv()

openAiclient = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

def format_answer(state):
    prompt = f"""
    The user asked:
    {state['user_request']}
    Action performed:
    {state['actions']}
    Observations:
    {state['observations']}
    Do not mention internal planning
    Do not mention state
    Do not mention tool
    """
    response = openAiclient.chat.completions.create(model=os.getenv("MODEL"),messages= [{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()

async def main():
    client = await connect()
    tools = await discover_tools(client)
    print()
    print("Available tools:")
    print("----------------------------------")
    for tool in tools:
        print(tool.name)
        print(tool.description)
    user_request = input("Please enter your action: ")
    state = await run_agent_loop(user_request, planner, execute_action, format_answer, tools, client)
    print("Final Answer: ", state.final_answer)


if __name__ == '__main__':
    asyncio.run(main())
