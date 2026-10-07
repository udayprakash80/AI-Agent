from fastmcp import Client
async def connect():
    """
    Connects to the MCP server.

    :return:
    """
    client = Client("server.py")
    await  client.__aenter__()
    print("Connected to MCP server")
    return client

async def disconnect(client):
    """
    Close the MCP connection.
    :param client:
    :return:
    """
    await client.__aexit__(
        None, None, None
    )

async def discover_tools(client):
    """Retrieve the list of tools available on the server."""
    tools = await client.list_tools()
    return tools

async def execute_tool(client, tool_name, arguments=None):
    """Execute a tool on the server."""
    if arguments is None:
        arguments = {}
    result = await client.call_tool(tool_name, arguments)
    return result