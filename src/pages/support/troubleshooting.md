---
title: Troubleshooting
description: Solutions to common issues encountered when setting up or using the Analytics MCP servers.
---

# Troubleshooting

Solutions to common issues encountered when setting up or using the Analytics MCP servers.

## Authentication and permissions

<AccordionItem slots="heading, text, text, text, text"/>

### "Authorization with the MCP server failed. You can check your credentials and permissions."

This issue can manifest itself in several ways, including:

* Authorization failed
* 403 forbidden
* `Omni.Tools.MCPAccess` permission error

**Cause:** Your account does not belong to a product profile that includes the **MCP Access** permission item.

**Fix:** Contact a system administrator or product administrator within your organization to add you to a product profile containing the **MCP Access** permission item. The contact within your organization is typically the individual or team that granted you initial access to Adobe Analytics or Customer Journey Analytics.

<AccordionItem slots="heading, text, text"/>

### "Your organization does not allow access to third-party applications"

**Cause:** Your account belongs to an IMS organization that blocks third-party app access by default.

**Fix:** Contact your Adobe Account Team.

<AccordionItem slots="heading, text, text"/>

### Wrong IMS org is active, or all results are null

**Cause:** The MCP inherits whichever org your browser was last logged into. If you were already authenticated, the org chooser is skipped automatically.

**Fix:** Log out of [CX Enterprise](https://experience.adobe.com), disconnect the MCP connector in your client, then reconnect. During reconnection you are prompted to choose your org.

## Connection and network issues

<AccordionItem slots="heading, text, text, text"/>

### TLS handshake failure or "Connection reset by peer" errors

**Cause:** A firewall or network proxy is potentially blocking traffic to Adobe authentication or analytics endpoints.

**Fix:** Work with your network team to allow the required Adobe IP addresses or domains:

* [Adobe Analytics IP addresses](https://experienceleague.adobe.com/en/docs/analytics/technotes/ip-addresses)
* [Adobe Analytics domains](https://experienceleague.adobe.com/en/docs/analytics/technotes/domains)
* [CX Enterprise IP addresses](https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/ip-addresses)
* [CX Enterprise domains](https://experienceleague.adobe.com/en/docs/core-services/interface/data-collection/domains)

## Data and reporting

<AccordionItem slots="heading, text, text"/>

### Agent uses a past year or incorrect date {#test}

**Cause:** Some AI models might default to their training cutoff date rather than the current date when interpreting relative date terms.

**Fix:** Explicitly state the full date or date range in your prompt rather than using relative terms like "this month" or "last quarter."

<AccordionItem slots="heading, text, text"/>

### Agent returns "Resource not found" for runReport, findDimensions, or findMetrics

**Possible cause:** Having both Adobe Analytics and Customer Journey Analytics connected simultaneously can cause some models to send requests to the wrong MCP server.

**Fix:** Disconnect both connectors and reconnect only the one you need for the current session.

## Project creation

<AccordionItem slots="heading, text, text"/>

### upsertProject fails with JSON validation errors

The project definition schema is complex, and some models might produce malformed JSON (especially in deeply nested structures).

**Workaround:** Provide the LLM with an existing valid project as a reference before prompting it to create a new one. Ask the LLM to compare its output against the reference before calling `upsertProject`.

<AccordionItem slots="heading, text, text"/>

### Project is created but shows an error banner when opened in Customer Journey Analytics

Common causes include malformed date ranges or incorrect grid position values on subPanels.

**Workaround:** Reference an existing project in the same data view when prompting. Include explicit examples of date range format and panel position values in your prompt.
