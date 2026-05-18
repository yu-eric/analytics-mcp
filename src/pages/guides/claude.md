---
title: Connect to Claude
description: Connect to Adobe Analytics and Customer Journey Analytics MCP servers using Claude.
---
# Connect to Claude

You can request Adobe Analytics and Customer Journey Analytics data using the Claude standalone application.

1. Ensure that your account has the [necessary permissions](index.md) to access the desired Analytics MCP server.
1. Log in to [Claude](https://claude.ai) using your credentials.
1. In the left menu, select the **Customize** icon.
1. Select **Connectors**, then select the **+** icon to add a connector.
1. Select the **Create app** button.
1. Give the connector a desired name (such as "Adobe Analytics" or "Customer Journey Analytics") and enter the desired MCP Server URL:
   * **Adobe Analytics**: `https://aa-mcp.adobe.io/mcp`
   * **Customer Journey Analytics**: `https://cja-mcp.adobe.io/mcp`
1. Once the connector is created, a login window pops up. Authenticate using your Adobe ID credentials. Ensure that you select the desired IMS org if your Adobe ID belongs to more than one.

The tool is ready for use. You can converse with Claude in context of your Analytics environment by invoking the tool:

```text
"Use the Adobe Analytics tool to show me what report suites are available."
"Use the Customer Journey Analytics tool to show me what data views are available."
```
