from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openAiclient = OpenAI(base_url=os.getenv('BASE_URL'), api_key=os.getenv('API_KEY'))

def decompose_task(user_request):
    prompt = f"""
You are an AI Task planner. Break the user's request into small tasks.
Rules:
1. create only the task necessary to complete the user's request.
2. Put the tasks in the correct execution order.
3. Each task should be a short action.
4. Return one task per line.
5. Do not number the tasks.
6. Do not explain the tasks.
CRITICAL RULE:
7.Return NO tasks (or "NONE") if the user request belongs to any of the following categories:
8. Greeting or casual conversation (e.g, "hi", "hello", "how are you?", "what's up?")
9. Introductions or personal details (e.g., "my name is udaya", "i am 25 years old", "i live in New York")
10. Personal opinions or preferences (e.g., "i like pizza", "my favorite color is blue", "i prefer cats over dogs")
11. Jokes or humor (e.g., "tell me a joke", "make me laugh", "why did the chicken cross the road?")
12. Small talk or chit-chat (e.g., "what's the weather like?", "how's your day going?", "what's new?")
13. Requests for personal advice or guidance (e.g., "what should I do?", "can you give me advice?", "what's the best way to handle this?")
14. Requests for personal information or data (e.g., "what's my account balance?", "can you tell me my location?", "what's my schedule for today?")
15. Requests for personal services or tasks (e.g., "can you book a flight for me?", "can you order food for me?", "can you schedule a meeting for me?")
16. Requests for personal opinions or recommendations (e.g., "what do you think about this?", "can you recommend a good restaurant?", "what's your opinion on this?")
17. Requests for personal entertainment or leisure activities (e.g., "can you play music for me?", "can you recommend a movie?", "what's a good book to read?", "can you suggest a fun activity?")
18. Requests for personal health or wellness advice (e.g., "what's a good workout routine?", "can you give me tips for healthy eating?", "what's the best way to manage stress?")
19. Requests for personal financial advice or guidance (e.g., "what's the best way to save money?", "can you give me investment advice?", "what's the best way to manage debt?")
20. Requests for personal legal advice or guidance (e.g., "what's the best way to handle a legal issue?", "can you give me legal advice?", "what's the best way to protect my rights?")
21. Requests for personal educational advice or guidance (e.g., "what's the best way to study for an exam?", "can you give me tips for learning a new skill?", "what's the best way to improve my grades?") 
22. Memory question about past interactions (e.g., "what did we talk about last time?", "can you remind me of our previous conversation?", "what's my history with you?")
23. Requests for personal travel advice or guidance (e.g., "what's the best way to plan a trip?", "can you give me travel recommendations?", "what's the best way to find cheap flights?")
24. Requests for personal shopping advice or guidance (e.g., "what's the best way to find deals?", "can you give me shopping recommendations?", "what's the best way to compare prices?")
25. Requests for personal technology advice or guidance (e.g., "what's the best way to troubleshoot a tech issue?", "can you give me tech recommendations?", "what's the best way to use a new device?")
26. Requests for personal social advice or guidance (e.g., "what's the best way to make friends?", "can you give me social tips?", "what's the best way to network?")
33. General knowledge/Q&A questions that can be answered directly without tools (e.g., "what is Machine Learning?", "who is the president of the United States?", "what is the capital of France?")
User request: {user_request}"""
    response = openAiclient.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "system", "content":"You are an AI task planner"}, {"role": "user", "content": prompt}])
    result = response.choices[0].message.content.strip()
    tasks = []
    for line in result.splitlines():
        line = line.strip()
        if line:
            tasks.append(line)
    return tasks
