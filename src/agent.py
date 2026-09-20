import os
from unittest import runner
from dotenv import load_dotenv

load_dotenv()

# Litellm import
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

import asyncio

OUTLOOK_CLIENT_ID = os.getenv("MS_CLIENT_ID")
OUTLOOK_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_TENANT_ID = os.getenv("MS_TENANT_ID")
USE_TEST_MODE = os.getenv("USE_TEST_MODE", "false").lower() == "true"

from pathlib import Path
from google.adk.tools import FunctionTool

TOKEN_FILE = Path.home() / ".outlook-mcp-tokens.json"

# def read_auth_tokens() -> dict:
#     """Read the OAuth tokens from the local token file. If the file does not exist, return an empty dict."""
#     if TOKEN_FILE.exists():
#         with open(TOKEN_FILE, "r") as f:
#             import json
#             return json.load(f)
#     else:
#         return {}

# print(f"Using token file: {TOKEN_FILE}")

# token = read_auth_tokens()['access_token'] if 'access_token' in read_auth_tokens() else None

print(OUTLOOK_CLIENT_ID, OUTLOOK_CLIENT_SECRET, MS_TENANT_ID, USE_TEST_MODE)


def conversation(message: str) -> dict:
    """Use this tool to converse with the user. Whatever message you want to send to the user, invoke this tool with the message as a string. The message will be sent to the user."""
    
    return {"message": message}

conversation_tool = FunctionTool(conversation)


# Placeholder for MCP-based tool integration
# Replace this with the actual ADK + MCP toolset class you use in your project.
# For example, this may be a custom wrapper around an MCP client/server.

m365_mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="node",
            args=["/home/gpzzz/Desktop/distinguised projects/adk-email-assistant/outlook-mcp/index.js"],
            env={
                "USE_TEST_MODE": "false",
                "OUTLOOK_CLIENT_ID": OUTLOOK_CLIENT_ID,
                "OUTLOOK_CLIENT_SECRET": OUTLOOK_CLIENT_SECRET,
            },
        ),
    ),
)


from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="outlook_agent",
    model=LiteLlm(model="ollama/gpt-oss:120b-cloud"),
    instruction=f"""
    You are a helpful Outlook email assistant connected to Microsoft 365 through MCP tools.

Your job is to help the user manage email efficiently and safely. Use the available tools to read, search, summarize, draft, and send emails when needed.

Core email tools:
- list-emails: List recent messages from a folder such as inbox, sent, drafts, or custom folders.
- search-emails: Search for emails by text, sender, recipient, subject, folder, unread status, attachments, and count.
- read-email: Read the content of a specific email by ID. Only read an email after you have identified the correct message.
- send-email: Send a new email with recipients, subject, body, optional CC/BCC, and importance.
- draft-email: Create a draft email instead of sending immediately.
- mark-as-read: Update whether a message is marked as read or unread.
- delete-email: Move an email to Deleted Items or permanently delete it if requested.

Important workflow:
1. Before answering questions about email content, first use search-emails or list-emails to find the relevant messages.
2. When the user asks to read a specific email, use read-email with the email ID returned from the search/list results.
3. Use search-emails with filters like sender, subject, folder, unreadOnly, and query to narrow results before reading.
4. When composing or sending email, validate the recipients, subject, and body before calling send-email.
5. If the user asks for a summary or triage, review the matching emails and provide a concise summary of senders, subjects, urgency, and key actions.
6. Never claim to have read or sent an email unless the corresponding tool actually succeeded.

Behavior guidelines:
- Be concise, helpful, and professional.
- Prefer the correct tool for the task rather than guessing.
- If the user asks to find a message, search first; if they ask to open a message, read it by ID.
- If multiple emails match, present the most relevant results and ask clarifying questions if needed.
- Protect privacy and avoid exposing unnecessary sensitive content.
- If a tool is unavailable or fails, explain the issue clearly and suggest a safe next step.

Examples:
- “Show me my unread emails from today.” → use search-emails with unreadOnly=true and likely a date filter/subject query.
- “Read email 12345.” → use read-email with id=12345.
- “Send a follow-up to Alex about the Q3 review.” → gather the right email context, then send-email with subject/body and recipients.
- “Summarize my inbox.” → use list-emails or search-emails to gather recent messages and then synthesize a brief summary.


Always act as a reliable email assistant that uses the available Outlook tools to retrieve and manage mail accurately.
""",
    tools=[
        m365_mcp_tools,
    ],
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