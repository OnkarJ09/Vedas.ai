# server.py
from mcp.server import FastMCP

server = FastMCP("demo-server")

@server.tool()
async def add_numbers(a: float, b: float) -> str:
    return f"{a + b}"

@server.resource("config://app")
async def get_app_config() -> str:
    return "App: demo, Version: 0.1.0, Status: Active"

@server.prompt()
async def assistant_prompt() -> str:
    return "You are a helpful assistant for demo. Be concise and friendly."

if __name__ == "__main__":
    server.run("stdio")
