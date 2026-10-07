from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

openAiclient = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))

def format_answer(state):
    prompt = f"""
    The user asked:
    {state['user_request']}
    Action performed:
    Tasks:
    {state['tasks']}
    Actions:
    {state['actions']}
    Observations:
    {state['observations']}
    Do not mention:
    - planner
    - agent loop
    - mcp
    - internal state
    - tools
    - internal reasoning
    """
    response = openAiclient.chat.completions.create(model=os.getenv("MODEL"),messages= [{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()