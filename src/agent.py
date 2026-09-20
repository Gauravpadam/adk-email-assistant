import os
from unittest import runner
from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

import asyncio

OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
OUTLOOK_CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
USE_TEST_MODE = os.getenv("USE_TEST_MODE", "false").lower() == "true"


# Placeholder for MCP-based tool integration
# Replace this with the actual ADK + MCP toolset class you use in your project.
# For example, this may be a custom wrapper around an MCP client/server.

m365_mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="node",
            args=["/workspaces/adk-email-assistant/outlook-mcp/index.js"],
            env={
                "USE_TEST_MODE": str(USE_TEST_MODE).lower(),
                "OUTLOOK_CLIENT_ID": OUTLOOK_CLIENT_ID,
                "OUTLOOK_CLIENT_SECRET": OUTLOOK_CLIENT_SECRET,
            },
        ),
    ),
)


root_agent = LlmAgent(
    name="adk_email_assistant",
    model="gemini-3.6-flash",
    instruction="""
You are a helpful email assistant.

Your job:
- summarize inbox content
- draft emails
- help triage incoming email
- suggest responses
- use MCP-connected tools to access email resources when available

If no email tool is connected yet, respond with a safe placeholder message
and explain that email tools will be wired through MCP.
    """,
    tools=[
        m365_mcp_tools
    ],
)
# 3. Instantiate the root agent
root_agent = LlmAgent(
    name="adk_email_assistant",
    model="gemini-3.6-flash",
    instruction="You are a helpful Outlook email assistant. Use tools to manage mail.",
    tools=[m365_mcp_tools],
)

# 4. Interactive CLI Runner Loop using ADK Sessions
async def run_cli_agent():
    # Setup session manager and create a single session for this terminal session
    session_service = InMemorySessionService()
    session_id = "local_developer_session"
    session = await session_service.create_session(
        app_name="outlook_cli_app",
        user_id="local_developer",
        session_id=session_id
    )

    
    # Initialize the Runner to orchestrate the agent and session context
    runner = Runner(
        app_name="outlook_cli_app",
        agent=root_agent,
        session_service=session_service
    )
    
    print("==================================================")
    print("Outlook Email Agent is Ready! (Session Established)")
    print("Type your message below. Type 'exit' or 'quit' to close.")
    print("==================================================")
    
    while True:
        try:
            # Get input inside the async loop
            user_query = input("\nYou: ")


            structured_message = Content(
                role="user",
                parts=[Part.from_text(text=user_query)]
            )

            
            if user_query.lower() in ["exit", "quit"]:
                print("Closing session. Goodbye!")
                break
                
            if not user_query.strip():
                continue
            
            print("Agent: *Thinking...*")
            
           # The correct way to execute a turn in the loop:
            event_stream = runner.run(
                session_id=session_id,
                user_id="local_developer",
                new_message=structured_message
            )
                
            # Safe execution stream parser
            for event in event_stream:
                # Check if it's the official final response event container
                if getattr(event, 'is_final_response', False):
                    print(f"\rAgent: {event.content}")
                
                # Fallback block: If the event itself is just a text chunk string
                elif isinstance(event, str):
                    # Print individual streaming string chunks on the same line
                    print(event, end="", flush=True)
                    
                # Fallback block: For standard chat event messages with a content payload
                elif hasattr(event, 'content'):
                    # Avoid printing user role entries by verifying it's from the model
                    if getattr(event, 'role', 'model') != 'user':
                        print(f"\nAgent: {event.content}")

        except Exception as e:
            print(f"\nExecution error: {e}")
                    
        except KeyboardInterrupt:
                print("\nSession interrupted. Goodbye!")
                break

if __name__ == "__main__":
    # Start the async execution loop
    try:
        asyncio.run(run_cli_agent())
    except Exception as initialization_error:
        print(f"Failed to boot framework runtime: {initialization_error}")