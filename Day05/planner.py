from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"))
def choose_tool(user_request):
    planner_prompt = f"""
    Your are a planner.
    Available tools:
    1. get_current_time
    Use when the user ask for the current date or time.
    2. roll_dice
    Use when the user ask for a random number or roll a dice.
    3. generate_password
    Use when the user ask for a password.
    if not tool is requested, return:
    none
    Return ONLY the tool name.
    User request: {user_request}
    """
    message = [{"role":"system", "content":"You are an AI planner"}, {"role": "user", "content": planner_prompt}]



    response = client.chat.completions.create(model=os.getenv("MODEL"), messages=message)
    return response.choices[0].message.content.strip()