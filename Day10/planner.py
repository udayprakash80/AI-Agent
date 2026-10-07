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
    return descriptions

def planner(state, tools):
    tool_descriptions = build_tool_description(tools)
    prompt = f"""
    You are AI Planner.
    Your job is to select the next task and the best tool to complete it.
    user request: {state['user_request']}
    tasks: {state['tasks']}
    Completed Actions: {state['actions']}
    Observations: {state['observations']}
    intermediate Results: {state['results']}
    Available tools: {tool_descriptions}
    Rules: 
    1. Select only ONE next action
    2. Select an action that helps complete a pending task.
    3. Never repeat a completed action unless necessary.
    4. User previous observations and intermediate results.
    5. If an action failed, choose another action. that can help complete the task.
    6. If all task are completed, return FINISH.
    7. Return ONLY the tool name or FINISH:
    8. Do not explain your answer.
    Next Decision:
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

