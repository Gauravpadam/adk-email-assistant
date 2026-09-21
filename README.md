# ADK Email Assistant

A lightweight Google ADK agent that connects to Microsoft Outlook through an MCP server. The Python app exposes a conversational email assistant, while the real mailbox access lives in the Node-based Outlook MCP server under `outlook-mcp/`.

## What this repo does

This project combines:

- Google ADK (`src/agent.py`) to create an LLM-powered agent
- Model Context Protocol (MCP) to expose external tools to the agent
- Microsoft Graph-backed Outlook integration in `outlook-mcp/` (via [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp))

In practice, the agent can ask the MCP server to:

- list emails
- read email content
- search mail
- send mail
- manage folders and rules
- work with calendar events
- optionally access OneDrive and Power Automate tools

## How it uses Outlook MCP

The ADK agent in `src/agent.py` creates an `McpToolset` that launches the MCP server as a stdio process:

```python
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
```

That means the Python agent does not call Microsoft Graph directly. Instead, it calls the MCP server, which exposes tools like `list-emails`, `search-emails`, `read-email`, and `send-email` over the standard MCP protocol.

The server side is implemented in `outlook-mcp/index.js` and registers all tool handlers from the modular folders under:

- `outlook-mcp/email/`
- `outlook-mcp/calendar/`
- `outlook-mcp/folder/`
- `outlook-mcp/rules/`
- `outlook-mcp/auth/`
- `outlook-mcp/onedrive/`
- `outlook-mcp/power-automate/`

## Repository layout

```text
.
├── src/
│   └── agent.py                # ADK agent + MCP connection
├── outlook-mcp/                # Node-based Outlook MCP server
│   ├── index.js                # MCP server entry point
│   ├── config.js               # env/config wiring
│   ├── auth/                   # OAuth flow and token handling
│   ├── email/                  # email listing/search/read/send tools
│   ├── calendar/               # event tools
│   ├── folder/                 # folder tools
│   ├── rules/                  # mailbox rule tools
│   ├── onedrive/               # file tools
│   ├── power-automate/         # flow integration
│   └── README.md               # detailed server docs
├── requirements.txt            # Python dependencies
└── README.md                   # this file
```

## Quick start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Outlook MCP server

In `outlook-mcp/`, copy the example env file and set your Azure app values:

```bash
cd outlook-mcp
cp .env.example .env
```

Set the values for:

- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_CLIENT_SECRET`
- `USE_TEST_MODE=false`

The server also expects Azure app registration settings used by the OAuth flow and Microsoft Graph API.

### 3. Configure the Python app

The ADK agent reads environment variables from the Python environment. In the current project this is usually loaded from `src/.env` and includes values such as:

- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_CLIENT_SECRET`
- `USE_TEST_MODE`

### 4. Run the agent

```bash
python src/agent.py
```

The agent boots the MCP server over stdio and then allows you to chat with it in the terminal.

## Typical workflow

1. The ADK agent starts the Node-based MCP server.
2. MCP exposes Microsoft 365 tools to the agent.
3. The user asks for something like “summarize my inbox” or “draft a response to this email”.
4. The agent calls the relevant MCP tool, such as `list-emails` or `read-email`.
5. The tool uses Microsoft Graph to access Outlook data.
6. The agent interprets the data and replies to the user.

## Notes on authentication

The MCP server handles OAuth and token persistence using the auth layer under `outlook-mcp/auth/`. It stores tokens locally, typically in a home-directory file such as:

```text
~/.outlook-mcp-tokens.json
```

This keeps the ADK layer thin: the agent simply calls tools, while the MCP server handles Graph auth and token management.
You will need to follow auth instructions in `

## Test mode

The server supports a `USE_TEST_MODE` flag for mock responses. This is useful for local development and validation when you do not want live Microsoft Graph calls.

## Important distinction

This repo is not the Outlook integration itself. It is the orchestration layer:

- `src/agent.py` = the AI agent and tool connector
- `outlook-mcp/` = the Outlook/Microsoft 365 MCP tool server

That split keeps the assistant logic separate from the API and auth plumbing, which is exactly what makes the repository easy to extend with more agents or tool servers.

## Further reading

For server-specific details, authentication setup, and tool breakdowns, see:

- `outlook-mcp/README.md`
- `outlook-mcp/.env.example`

## License

This project is currently configured for local development and experimentation around MCP-based Outlook access.
