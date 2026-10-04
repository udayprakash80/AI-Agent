import random
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("Time Server")

@mcp.tool()
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def roll_dice():
    """Rolls a dice and returns a random number between 1 and 6."""
    return random.randint(1,6)

@mcp.tool()
def generate_password(length=8):
    """Generates a random password of the specified length."""
    import secrets
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("Server is running...")
    mcp.run()