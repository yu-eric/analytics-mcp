---
title: Connect to ChatGPT
description: Connect to Adobe Analytics and Customer Journey Analytics MCP servers using ChatGPT.
---
# Connect to ChatGPT

You can request Adobe Analytics and Customer Journey Analytics data using ChatGPT.

<InlineAlert variant="warning" slots="text"/>

You must be on the "Plus" or "Pro" subscription to ChatGPT. OpenAI does not allow connecting to MCP servers using their "Free" tier.

1. Ensure that your account has the [necessary permissions](index.md) to access the desired Analytics MCP server.
1. Log in to [ChatGPT](https://chatgpt.com) using your credentials.
1. In the lower left, select **your name** &rarr; **Settings**.
1. Select **Apps**, then enable **Developer mode**.
1. Select the **Create app** button.
1. Give the app a desired name (such as "Adobe Analytics" or "Customer Journey Analytics") and enter the desired MCP Server URL:
   * **Adobe Analytics**: `https://aa-mcp.adobe.io/mcp`
   * **Customer Journey Analytices**: `https://cja-mcp.adobe.io/mcp`
1. Ensure that Authentication is set to **OAuth** (set by default), and select the acceptance check box to continue.
1. Once the app is created, a login window pops up. Authenticate using your Adobe ID credentials. Ensure that you select the desired IMS org if your Adobe ID belongs to more than one.

The tool is ready for use. You can converse with ChatGPT in context of your Analytics environment by invoking the tool:

```text
"Use the Adobe Analytics tool to show me what report suites are available."
"Use the Customer Journey Analytics tool to show me what data views are available."
```
