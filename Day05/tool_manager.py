from tools import (get_current_time, random_number, generate_password)

def execute_tool(user_input):
    text = user_input.lower()
    if text == "get_current_time":
        return get_current_time()
    elif text == "roll_dice":
        return random_number()
    elif text == "generate_password":
        return generate_password()
    return None