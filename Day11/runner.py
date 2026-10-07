import asyncio
from memory import create_database
from answer import format_answer
from planner import planner
from executer import execute_action
from loop import run_agent_loop
from mcp_client import*

async def main():
    create_database()
    client = await connect()
    tools = await discover_tools(client)
    print()
    print("Available tools:")
    print("----------------------------------")
    for tool in tools:
        print(tool.name)
    user_request = input("Please enter your action: ")
    state = await run_agent_loop(user_request, planner, execute_action, format_answer, tools, client)
    print("Final Answer: ", state["final_answer"])

if __name__ == '__main__':
    asyncio.run(main())
