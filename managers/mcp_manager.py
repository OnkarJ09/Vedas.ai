import os
import asyncio
import logging
from dotenv import load_dotenv
from mcp_use import MCPClient, MCPAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.base import BaseCallbackHandler

# Silence mcp_use logs except warnings/errors
logging.getLogger("mcp_use").setLevel(logging.WARNING)
logging.getLogger("mcp_use.telemetry").setLevel(logging.ERROR)

# Streaming handler for LLM tokens
class StreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)

async def run_agent(client):
    """Run MCP agent with streaming LLM output."""
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        # streaming=True,
        callbacks=[StreamHandler()]
    )

    agent = MCPAgent(
        llm=gemini_llm,
        client=client,
        max_steps=20,
        use_server_manager=True
    )

    result = await agent.run("Add 8 and 15 using the math tool", max_steps=10)

async def run_tool_direct(client):
    """Run tool directly with streaming results."""
    print("\n--- Direct Tool Mode (streaming tool) ---")
    async for chunk in client.run_tool(
        "add_numbers",
        {"a": 8, "b": 15},
        server_name="add_numbers",
        stream=True
    ):
        print(chunk, end="")

async def main():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is not set")

    client = MCPClient.from_config_file("multi_server_config.json")

    # Choose mode here
    await run_agent(client)       # Agent reasoning (streaming tokens)
    # await run_tool_direct(client) # Direct tool call (streaming chunks)

    """
        You can enable it if you want the manual closing of servers instead of
        default way in which python closes them and exit the servers
        """
    # Clean shutdown (closes any spawned MCP server processes)
    # try:
    #     await client.close_all_sessions()
    # except Exception as e:
    #     print("Cleanup warning:", e)

if __name__ == "__main__":
    asyncio.run(main())
