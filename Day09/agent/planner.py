from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

def build_tool_description(tools):
    # print('Tools', tools)
    descriptions = ""
    for tool in tools:
        descriptions += f"""
        Tool Name: {tool.name}
        Description: {tool.description}
        __________________________________
    """
        # print('descriptions', descriptions)
    return descriptions

def planner(state, tools):
    tool_descriptions = build_tool_description(tools)
    prompt = f"""
    You are AI Planner.
    Your job is to decide ONLY the next action.
    user request: {state['user_request']}
    Completed actions: {state['actions']}
    Previous observations: {state['observations']}
    Available tools: {tool_descriptions}
    Rules: 
    1. Choose only ONE next action.
    2. Never repeat the same action that has already been completed.
    3. Use the observation to make a decide what is still required.
    4. If user's request has been completely satisfied, return "FINISH" as the next action.
    5. Return the tool name or FINISH.
    6. Do not explain
    Next Action:
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

