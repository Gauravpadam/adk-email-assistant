## Summarize emails:

```
You: Summarise my emails
Agent: *Thinking...*
Error cleaning up session stdio_session: original event loop is closed, resources may be leaked.
Failed to parse JSONRPC message from server
Traceback (most recent call last):
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/mcp/client/stdio.py", line 221, in _parse_line
    message = types.jsonrpc_message_adapter.validate_json(line, by_name=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/pydantic/type_adapter.py", line 492, in validate_json
    return self.validator.validate_json(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for union[JSONRPCRequest,JSONRPCNotification,JSONRPCResponse,JSONRPCError]
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='Using home directory: /home/gpzzz', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
STARTING M365-ASSISTANT MCP SERVER
Test mode is disabled
m365-assistant connected and listening
REQUEST: tools/list [2]
TOOLS LIST REQUEST: ID [2]
TOOLS COUNT: 34
TOOLS NAMES: about, authenticate, check-auth-status, list-events, decline-event, create-event, cancel-event, delete-event, list-emails, search-emails, read-email, send-email, draft-email, mark-as-read, delete-email, list-folders, create-folder, move-emails, list-rules, create-rule, edit-rule-sequence, onedrive-list, onedrive-search, onedrive-download, onedrive-upload, onedrive-upload-large, onedrive-share, onedrive-create-folder, onedrive-delete, flow-list-environments, flow-list, flow-run, flow-list-runs, flow-toggle
Agent: parts=[Part(
  text='We need to call check-auth-status.'
), Part(
  function_call=FunctionCall(
    args={},
    id='adk_tool_call_a8164e724a67479da2ae84ded16b3687',
    name='check-auth-status'
  )
), Part(
  function_call=FunctionCall(
    args={},
    id='adk_tool_call_e2235c3e98e241adb47480670f233331',
    name='check-auth-status'
  )
)] role='model'
REQUEST: tools/call [3]
TOOL CALL: check-auth-status
[CHECK-AUTH-STATUS] Starting authentication status check
[CHECK-AUTH-STATUS] Tokens loaded: YES
[CHECK-AUTH-STATUS] Access token present
[CHECK-AUTH-STATUS] Token expires at: 1789971953681
[CHECK-AUTH-STATUS] Current time: 1789968382698
REQUEST: tools/call [4]
TOOL CALL: check-auth-status
[CHECK-AUTH-STATUS] Starting authentication status check
[CHECK-AUTH-STATUS] Tokens loaded: YES
[CHECK-AUTH-STATUS] Access token present
[CHECK-AUTH-STATUS] Token expires at: 1789971953681
[CHECK-AUTH-STATUS] Current time: 1789968382700
Agent: parts=[Part(
  function_response=FunctionResponse(
    id='adk_tool_call_a8164e724a67479da2ae84ded16b3687',
    name='check-auth-status',
    response={
      'content': [
        {
          'text': 'Authenticated and ready',
          'type': 'text'
        },
      ],
      'isError': False
    }
  )
), Part(
  function_response=FunctionResponse(
    id='adk_tool_call_e2235c3e98e241adb47480670f233331',
    name='check-auth-status',
    response={
      'content': [
        {
          'text': 'Authenticated and ready',
          'type': 'text'
        },
      ],
      'isError': False
    }
  )
)] role='user'
Agent: parts=[Part(
  text='We will call list-emails.'
), Part(
  function_call=FunctionCall(
    args={
      'count': 10,
      'folder': 'inbox'
    },
    id='adk_tool_call_ad2417ad467e475db4c00bcb6550e1a4',
    name='list-emails'
  )
)] role='model'
REQUEST: tools/call [5]
TOOL CALL: list-emails
Tokens loaded from file.
Using well-known folder path for "inbox"
Making real API call: GET me/mailFolders/inbox/messages
Query string: ?%24top=10&%24orderby=receivedDateTime+desc&%24select=id%2Csubject%2Cfrom%2CtoRecipients%2CccRecipients%2CreceivedDateTime%2CbodyPreview%2ChasAttachments%2Cimportance%2CisRead
Full URL: https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?%24top=10&%24orderby=receivedDateTime+desc&%24select=id%2Csubject%2Cfrom%2CtoRecipients%2CccRecipients%2CreceivedDateTime%2CbodyPreview%2ChasAttachments%2Cimportance%2CisRead
Pagination: Retrieved 1 items, total so far: 1
Pagination complete: Retrieved 1 total items
Agent: parts=[Part(
  function_response=FunctionResponse(
    id='adk_tool_call_ad2417ad467e475db4c00bcb6550e1a4',
    name='list-emails',
    response={
      'content': [
        {
          'text': """Found 1 emails in inbox:

1. [UNREAD] 7/27/2014, 5:56:55 AM - From: Outlook.com Team (member_services@outlook.com)
Subject: Getting started with your mail account
ID: AQMkADAwATM0MDAAMS1jMjE2LWY4YzMtMDACLTAwCgBGAAADhbc5zSoaHkqokvZgQCQnaAcAHfkOZBtECka9OWX9cZffGAAAAgEMAAAAHfkOZBtECka9OWX9cZffGAAAAgVQAAAA
""",
          'type': 'text'
        },
      ],
      'isError': False
    }
  )
)] role='user'
Agent: parts=[Part(
  text="""Here’s a quick summary of the messages currently in your inbox:

| # | Date & Time (UTC) | From | Subject | Status |
|---|-------------------|------|---------|--------|
| 1 | 2014‑07‑27 05:56:55 | Outlook.com Team (member_services@outlook.com) | **Getting started with your mail account** | **Unread** (ID: `AQMkADAwATM0MDAAMS1jMjE2LWY4YzMtMDACLTAwCgBGAAADhbc5zSoaHkqokvZgQCQnaAcAHfkOZBtECka9OWX9cZffGAAAAgEMAAAAHfkOZBtECka9OWX9cZffGAAAAgVQAAAA`) |

**Key points**

- Only one email is present, and it is still unread.
- It appears to be an introductory or welcome message from the Outlook.com team about getting started with your mail account.

**Next steps you might consider**

- Open and read the email to see the onboarding instructions.
- Mark it as read or move it to a folder (e.g., “Welcomes”) if you’d like to keep it organized.
- Reply or follow‑up if you have any questions about the account setup.

Would you like me to read the full content of this email, move it, mark it as read, or anything else?"""
)] role='model'
```

## Write an email to someone
```
You: Write an email to aadish.jain@techolution.com saying hi and this was written by assistant
Agent: *Thinking...*
/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/google/adk/tools/mcp_tool/mcp_toolset.py:401: UserWarning: [EXPERIMENTAL] feature FeatureName._MCP_GRACEFUL_ERROR_HANDLING is enabled.
  session = await self._mcp_session_manager.create_session(
Failed to parse JSONRPC message from server
Traceback (most recent call last):
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/mcp/client/stdio.py", line 221, in _parse_line
    message = types.jsonrpc_message_adapter.validate_json(line, by_name=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/pydantic/type_adapter.py", line 492, in validate_json
    return self.validator.validate_json(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for union[JSONRPCRequest,JSONRPCNotification,JSONRPCResponse,JSONRPCError]
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='Using home directory: /home/gpzzz', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
STARTING M365-ASSISTANT MCP SERVER
Test mode is disabled
m365-assistant connected and listening
REQUEST: tools/list [2]
TOOLS LIST REQUEST: ID [2]
TOOLS COUNT: 34
TOOLS NAMES: about, authenticate, check-auth-status, list-events, decline-event, create-event, cancel-event, delete-event, list-emails, search-emails, read-email, send-email, draft-email, mark-as-read, delete-email, list-folders, create-folder, move-emails, list-rules, create-rule, edit-rule-sequence, onedrive-list, onedrive-search, onedrive-download, onedrive-upload, onedrive-upload-large, onedrive-share, onedrive-create-folder, onedrive-delete, flow-list-environments, flow-list, flow-run, flow-list-runs, flow-toggle
/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/google/adk/features/_feature_decorator.py:71: UserWarning: [EXPERIMENTAL] feature FeatureName.BASE_AUTHENTICATED_TOOL is enabled.
  check_feature_enabled()
/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/google/adk/models/llm_request.py:298: UserWarning: [EXPERIMENTAL] feature FeatureName.JSON_SCHEMA_FOR_FUNC_DECL is enabled.
  declaration = tool._get_declaration()
Agent: parts=[Part(
  text='Would you like me to send this email now, or should I just create and save it as a draft?'
)] role='model'

You: Send it
Agent: *Thinking...*
Error cleaning up session stdio_session: original event loop is closed, resources may be leaked.
Failed to parse JSONRPC message from server
Traceback (most recent call last):
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/mcp/client/stdio.py", line 221, in _parse_line
    message = types.jsonrpc_message_adapter.validate_json(line, by_name=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gpzzz/miniconda3/envs/adk-dev/lib/python3.11/site-packages/pydantic/type_adapter.py", line 492, in validate_json
    return self.validator.validate_json(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for union[JSONRPCRequest,JSONRPCNotification,JSONRPCResponse,JSONRPCError]
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='Using home directory: /home/gpzzz', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
STARTING M365-ASSISTANT MCP SERVER
Test mode is disabled
m365-assistant connected and listening
REQUEST: tools/list [2]
TOOLS LIST REQUEST: ID [2]
TOOLS COUNT: 34
TOOLS NAMES: about, authenticate, check-auth-status, list-events, decline-event, create-event, cancel-event, delete-event, list-emails, search-emails, read-email, send-email, draft-email, mark-as-read, delete-email, list-folders, create-folder, move-emails, list-rules, create-rule, edit-rule-sequence, onedrive-list, onedrive-search, onedrive-download, onedrive-upload, onedrive-upload-large, onedrive-share, onedrive-create-folder, onedrive-delete, flow-list-environments, flow-list, flow-run, flow-list-runs, flow-toggle
Agent: parts=[Part(
  function_call=FunctionCall(
    args={
      'body': """Hi,

This was written by assistant.""",
      'isHtml': False,
      'subject': 'Hi',
      'to': 'aadish.jain@techolution.com'
    },
    id='call_6a308e3d-72fc-4afb-9dd8-a098e3059dde',
    name='send-email'
  )
)] role='model'
REQUEST: tools/call [3]
TOOL CALL: send-email
Tokens loaded from file.
Making real API call: POST me/sendMail
Full URL: https://graph.microsoft.com/v1.0/me/sendMail
Agent: parts=[Part(
  function_response=FunctionResponse(
    id='call_6a308e3d-72fc-4afb-9dd8-a098e3059dde',
    name='send-email',
    response={
      'content': [
        {
          'text': """Email sent successfully!

Subject: Hi
Recipients: 1
Message Length: 35 characters""",
          'type': 'text'
        },
      ],
      'isError': False
    }
  )
)] role='user'
Agent: parts=[Part(
  text='Your email to\u202faadish.jain@techolution.com\u202fhas been sent successfully. Let me know if there’s anything else I can help you with!'
)] role='model'
```