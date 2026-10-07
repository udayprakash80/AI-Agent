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
    Your job is to decide the next task and the tool required to complete that task.
    user request: {state['user_request']}
    Relevant Previous Memories: {state['memories']}
    Tasks: {state['tasks']}
    Pending Tasks:
    {[
        item["task"]
        for item in state["tasks"]
        if item["status"] == "pending"
    ]}
    Completed Actions: {state['actions']}
    Observations: {state['observations']}
    intermediate Results: {state['results']}
    Available tools: {tool_descriptions}
    Rules: 
    1. Select only ONE pending task
    2. The TASK must be copied EXACTLY from the pending task list.
    3. Do not change the task wording.
    4. Do not select a completed task.
    5. Select the best available tool form that task.
    6. Use previous observations and relevant memories.
    7. If an action failed, reconsider the task.
    8. If there are no pending tasks, return ONLY the word:
    FINISH
    9. IF tasks are still pending, return exactly two lines in this format: 
    TASK: <exact pending task>
    TOOL: <tool_name>
    10. Do not explain anything.
    11. IF the request can be answered directly using conversational memory, standard knowledge, or if tasks list is 
    empty/NONE, respond ONLY with: FINISH.
    12. IF a tool is required to complete a pending task, respond strictly in this format:
    TASK: <task description> 
    TOOL: <exact tool name from Available Tools>
    13. NEVER output "TOOL: none" or invent tool names. if no valid tool from Available Tools is needed, respond with FINISH.
    
    Next Decision:
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

