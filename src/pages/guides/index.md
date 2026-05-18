---
title: Getting started with Analytics MCP servers
description: Connect Adobe Analytics and Customer Journey Analytics MCP servers to supported LLM clients.
---

# Get started

Connect an Adobe Analytics or Customer Journey Analytics MCP server to a supported LLM client. Once connected, you can query your analytics data conversationally, letting the LLM retrieve reports, components, and more, on your behalf.

Before using these MCP tools, ensure that you have the correct permissions. Have a system administrator or product administrator within your organization grant you the appropriate permissions in the [Adobe Admin Console](https://adminconsole.adobe.com):

* Your account must belong to a product profile containing the **MCP Access** permission item. *This requirement applies to all users, including product administrators.*
* Your account must have the Adobe Analytics or Customer Journey Analytics permissions required for the actions that you want to take. MCP servers enforce the same permissions as the UI.

## MCP server URLs

Use the following URLs when configuring your MCP client:

* **Adobe Analytics (Beta)**: `https://mcp-gateway.adobe.io/aa/mcp`
* **Adobe Analytics (Production)**: `https://aa-mcp.adobe.io/mcp`
* **Customer Journey Analytics (Beta)**: `https://mcp-gateway.adobe.io/cja/mcp`
* **Customer Journey Analytics (Production)**: `https://cja-mcp.adobe.io/mcp`

## Choose your client

Each guide walks through the full setup for a specific client:

<Product-Card slots="icon, heading, text, buttons" />

![ChatGPT icon](../assets/OpenAI-black-monoblossom.svg)

### ChatGPT

Connect through Settings > Apps. Requires a Plus or Pro subscription.

* [Setup guide](chatgpt.md)

<Product-Card slots="icon, heading, text, buttons" />

![Claude icon](../assets/Claude_AI_symbol.svg)

### Claude

Connect through the Connectors menu in the Claude web app.

* [Setup guide](claude.md)

<Product-Card slots="icon, heading, text, buttons" />

![Cursor icon](../assets/CUBE_25D.svg)

### Cursor

Configure a `mcp.json` file in the Cursor IDE.

* [Setup guide](cursor.md)

<Product-Card slots="icon, heading, text" />

![Gemini icon](../assets/Google_Gemini_icon.svg)

### Gemini

CLI-only support; guide forthcoming.

<Product-Card slots="icon, heading, text" />

![Copilot icon](../assets/Microsoft_Copilot_Icon.svg)

### Copilot

Not yet available. Support is planned.

<Product-Card slots="icon, heading, text, buttons" />

![OAuth icon](../assets/Oauth_logo.svg)

### OAuth server-to-server

Connect programmatically without a UI client using OAuth server-to-server credentials.

* [Setup guide](oauth.md)

## Switching IMS organizations

If your Adobe ID belongs to multiple IMS organizations, IMS automatically logs you into the organization that you already have an active session with instead of showing the organization chooser. To switch to a different organization, follow these steps:

1. Disconnect the MCP connector in your client. You do not need to remove it.
1. Log out of your current Adobe session in your browser.
1. Reconnect the MCP connector in your client. The login flow presents the organization chooser, allowing you to select the desired organization.
