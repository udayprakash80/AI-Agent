from tools import (get_current_time, random_number, generate_password)

def execute_tool(user_input):
    text = user_input.lower()
    if "time" in text or "clock" in text:
        return get_current_time()
    elif "random" in text or "dice" in text:
        return random_number()
    elif "password" in text or "pass" in text:
        return generate_password()
    return None