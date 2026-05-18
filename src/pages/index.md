---
title: Analytics MCP servers
description: Overview of available MCP servers for Adobe Analytics and Customer Journey Analytics.
---

<Superhero slots="image, heading, text, buttons" background="rgb(37, 37, 37)"/>

![Hero image](assets/platform-hero.png)

# Analytics MCP servers

MCP servers for Adobe Analytics and Customer Journey Analytics.

[Get started](guides/index.md)

<Resources slots="heading, links"/>

#### Resources

* [Quick start guide](guides/index.md)
* [Adobe Analytics MCP tool reference](aa/reference.md)
* [Customer Journey Analytics MCP tool reference](cja/reference.md)
* [Github repository](https://github.com/AdobeDocs/analytics-mcp)

## Overview

This documentation covers the Adobe-hosted MCP servers for Adobe Analytics and Customer Journey Analytics. These servers connect MCP-compatible clients (like Claude, ChatGPT, or Cursor) directly to your analytics environment. Once connected, your client can invoke product-specific tools to query data, explore trends, build segments, and manage components using natural language as part of an LLM or agent-driven workflow.

Both servers share a standardized connection model with consistent endpoints and a common onboarding flow. See [Getting started](guides/index.md) to learn how to connect the desired MCP server to your agent of choice, or the [Adobe Analytics](aa/reference.md) or [Customer Journey Analytics](cja/reference.md) tool references to explore each server's capabilities.

## Additional Information

If you are looking for analytics data collection strategies for your own MCP servers, see [Collect analytics and apply personalization in MCP clients](https://experienceleague.adobe.com/en/docs/experience-platform/collection/use-cases/mcp/chatgpt) in the Adobe Experience Platform Data Collection documentation.

This user guide adheres to Adobe's Code of Conduct. Contributions are encouraged and appreciated. See Adobe's [Code of Conduct](https://github.com/AdobeDocs/analytics-mcp/blob/main/CODE_OF_CONDUCT.md) and [Contribution Guidelines](https://github.com/AdobeDocs/analytics-mcp/blob/main/.github/CONTRIBUTING.md) on GitHub for more information.

<InlineAlert variant="warning" slots="text, text, text"/>

The Model Context Protocol (MCP) is an emerging open-source standard that can introduce security and reliability risks. Adobe's MCP server integrations and related documentation are provided "as is," without warranties of any kind.

Connecting MCP clients or servers to Adobe products is a customer-elected configuration. Customers are responsible for evaluating the security and suitability of any MCP integration. Adobe is not responsible for issues arising from misconfiguration, misuse, third-party vulnerabilities, or unintended actions performed through MCP-enabled workflows.

To reduce risk, test integrations in a sandbox environment before production use. Validate all MCP-initiated actions and responses before acting on them.
