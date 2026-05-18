---
title: Frequently asked questions
description: Answers to common questions about the Analytics MCP servers.
---

<HeroSimple slots="heading" background="white" textColor="black"/>

# Frequently asked questions

Common questions about setting up and using the Analytics MCP servers.

## Getting started

<AccordionItem slots="heading, text"/>

### What permissions are required to use the MCP servers?

Users must be added to an [Adobe Admin Console](https://adminconsole.adobe.com) product profile that includes the **MCP Access** permission item. *This requirement applies to all users, including product administrators.*

<AccordionItem slots="heading, text"/>

### What authentication methods are supported?

The MCP servers use OAuth DCR, which is handled automatically by supported LLM clients during the browser-based login flow. For programmatic (server-to-server) access, a Bearer token obtained using the OAuth server-to-server flow is required. User tokens are required; service tokens are not supported.

<AccordionItem slots="heading, text"/>

### How do I switch between IMS orgs?

Log out of [experience.adobe.com](https://experience.adobe.com), disconnect the MCP connector in your client, then reconnect. You are prompted to choose your org during reconnection.

<AccordionItem slots="heading, text"/>

### Can I use the Analytics MCP servers with multiple IMS orgs?

Yes, but only one org is active at a time. The selected org is determined during the authentication flow. To switch orgs, follow the logout and reconnect process described above.

## Cost and licensing

<AccordionItem slots="heading, text"/>

### Is there an additional cost to use the Analytics MCP servers?

No. The Analytics MCP servers are available at no extra cost for all Adobe Analytics and Customer Journey Analytics customers. MCP report calls count toward your existing monthly report request allowance. Contact your Adobe Account Team to increase your organization's reporting request allowance.

## Features and capabilities

<AccordionItem slots="heading, text"/>

### Does the MCP server make any LLM calls on its own?

No. The Analytics MCP servers only call Adobe Analytics and Customer Journey Analytics APIs. They do not make LLM calls on their own. You connect your own LLM client to the MCP server.

<AccordionItem slots="heading, text"/>

### Can I make admin changes through the MCP, like editing data views or managing report suites?

Not currently. The Analytics MCP servers are focused on reporting and analysis use cases at this time.

<AccordionItem slots="heading, text, text"/>

### Are there any limitations to runReport compared to the reporting API?

The `runReport` MCP tool has mostly comparable feature parity with reporting API capabilities.

The current primary limitation with the MCP tool is that it currently returns up to 100 rows per call and does not expose a pagination parameter. Apply filters or narrow your query scope to work within this limit.

<AccordionItem slots="heading, text"/>

### Does the MCP support scheduling reports?

Not currently. The Adobe Analytics and Customer Journey Analytics UIs are the recommended paths for scheduled report delivery.

<AccordionItem slots="heading, text"/>

### Is there a size limit for upsertProject payloads?

No limit is enforced at the MCP layer. Practical limits come from the AI client's context window and the underlying API that the MCP tool uses.

<AccordionItem slots="heading, text"/>

### How do the MCP servers sort components returned by findMetrics and findDimensions?

Semantic search is enabled for both tools. Results are ranked by how recently and frequently you have used a component, weighted more heavily toward your personal usage history than your organization's overall usage.

<AccordionItem slots="heading, text"/>

### Are the Analytics MCP servers available in all regions?

Yes. The current MCP URLs automatically route each request to the nearest region based on your IMS org.

## Data and privacy

<AccordionItem slots="heading, text"/>

### Is my data used to train AI models?

The answer to this question depends on your agreement with the LLM provider, not Adobe. For enterprise or API deployments, both Anthropic (Claude) and OpenAI (ChatGPT) state that customer data is not used to train models by default. Review your LLM provider's enterprise data terms for an authoritative answer.

<AccordionItem slots="heading, text"/>

### Who controls data access when using the MCP?

System administrators and product administrators determine which users can access the Analytics MCP servers. These administrators control access using the [Adobe Admin Console](https://adminconsole.adobe.com), specifically by adding or removing users to product profiles containing the **MCP Access** permission item. When a user connects an external LLM to the MCP server, that LLM can access the same data that the user is authorized to see. Adobe recommends that organizations review their LLM provider's data handling policies before granting users MCP access.
