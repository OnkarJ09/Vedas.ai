import os
import asyncio
from dotenv import load_dotenv
from mcp_use import MCPClient, MCPAgent
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logging.getLogger("mcp_use").setLevel(logging.WARNING)
logging.getLogger("mcp_use.telemetry").setLevel(logging.ERROR)


async def mcp_manager():
    # Load .env if present and ensure GOOGLE_API_KEY is in the environment
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is not set")

    # Configure your MCP servers (same structure used in examples)
    client = MCPClient.from_config_file("multi_server_config.json")

    # Use a current Gemini model; "gemini-2.5-flash" also works if enabled on your key
    gemini_llm = ChatGoogleGenerativeAI(model=os.getenv("DEFAULT_MODEL"))

    # Create the agent; enable dynamic server routing here
    agent = MCPAgent(
        llm=gemini_llm,
        client=client,
        max_steps=20,
        use_server_manager=True
    )

    # Agent runs – dynamic server selection
    result_dynamic = await agent.run(
        "Add 8 and 15 using the math tool",
        max_steps=10
    )

    # It is for testing purpose
    # Agent runs with explicit server selection
    # result_demo = await agent.run("Please add 100 and 200", server_name="demo")
    # print("Explicit 'demo' server result:", result_demo)

    """
    You can enable it if you want the manual closing of servers instead of
    default way in which python closes them and exit the servers
    """
    # Clean shutdown (closes any spawned MCP server processes)
    # try:
    #     await client.close_all_sessions()
    # except Exception as e:
    #     print("Cleanup warning:", e)

    return str(result_dynamic)

if __name__ == "__main__":
    asyncio.run(mcp_manager())
