---
title: Connect using OAuth
description: Connect to Adobe Analytics and Customer Journey Analytics MCP servers using a server-to-server OAuth workflow.
---
# Use OAuth to connect

Use an OAuth server-to-server access token to connect programmatically to the Adobe Analytics or Customer Journey Analytics MCP servers. This page outlines the requirements and walks through the connection workflow.

## Requirements

Before connecting, you need an Adobe Developer Console project with [OAuth server-to-server credentials](https://developer.adobe.com/developer-console/docs/guides/authentication/ServerToServerAuthentication/) and an [IMS access token](https://developer.adobe.com/developer-console/docs/guides/authentication/ServerToServerAuthentication/implementation/) generated using the `client_credentials` grant type. Ensure that the technical account is assigned to a product profile containing the **MCP Access** permission item.

Each request to the MCP server requires the following headers:

| Header | Description | CJA | AA |
| --- | --- | --- | --- |
| `Authorization` | Bearer token using your IMS access token | Required | Required |
| `x-gw-ims-org-id` | Your IMS Organization ID | Required | Required |
| `x-api-key` | Your OAuth client ID | Required | Required |
| `x-global-company-id` | Your global company ID | -- | Required |

Send these headers to the endpoint for your product:

* **Adobe Analytics**: `https://aa-mcp.adobe.io/mcp`
* **Customer Journey Analytics**: `https://cja-mcp.adobe.io/mcp`

## Connect to the MCP server

Set the required headers and open a connection using the `streamable-http` transport. The following pseudocode demonstrates the workflow:

```text
# Configuration
MCP_URL = "https://mcp-gateway.adobe.io/cja/mcp"  # or /aa/mcp for Adobe Analytics
ORG_ID = "<IMS_ORGANIZATION_ID>"
CLIENT_ID = "<CLIENT_ID>"

# Set required headers
headers = {
  "Authorization": "Bearer <ACCESS_TOKEN>",
  "x-gw-ims-org-id": ORG_ID,
  "x-api-key": CLIENT_ID
}

# For Adobe Analytics, also include:
# headers["x-global-company-id"] = "<GLOBAL_COMPANY_ID>"

# Open an MCP client connection using streamable-http
client = MCPClient(
  transport = "streamable-http",
  url       = MCP_URL,
  headers   = headers
)

# Interact with the server
client.ping()
tools  = client.tools.list()
result = client.tools.call("tool_name", {"param": "value"})
```

## Token refresh

Access tokens expire after the duration specified in the `expires_in` field of the token response. To maintain an active connection:

* Cache the access token and track its expiration time.
* Refresh the token before it expires to avoid interruptions.
* If you receive a `401 Unauthorized` response, request a new token, update your headers, reconnect, and retry the request.

See the [token generation guide](https://developer.adobe.com/developer-console/docs/guides/authentication/ServerToServerAuthentication/implementation/) for details on requesting and refreshing access tokens.
