from datetime import datetime
import random
import secrets

def greet(name):
    return f"Hello {name}!"

def get_current_time():
    return datetime.now()

def random_number():
    return random.randint(1,6)

def generate_password(length=8):
    return secrets.token_urlsafe(length)

def read_text_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{filename}' not found."


