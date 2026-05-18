---
title: Adobe Analytics MCP server tool reference
description: A complete reference of all tools available in the Adobe Analytics MCP server, including descriptions, parameters, and usage details.
---

# Adobe Analytics MCP server tool reference

The following tools are available when connected to the Adobe Analytics MCP server. Each tool can be invoked by an LLM client to interact with your Adobe Analytics data, components, and workspace projects. Most tools accept optional `globalCompanyId` and `reportSuiteId` parameters; if omitted, the server uses the session defaults set with `setSessionDefaults`.

## Setup and guides

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Adobe Analytics (`describeAa`)

The starting point for learning how to use the Adobe Analytics MCP tools. Returns focused reference guides covering tool usage, available dimensions and metrics, segment definition syntax, calculated metric definition syntax, organizational context, and workspace project definitions. Call this tool before creating segments, calculated metrics, or workspace projects to learn the required structures.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `guideType` | No | String (enum) | The type of guide to return. If omitted, returns the default AA reference guide. Valid values include:\<br/>• `AA_REFERENCE_GUIDE` (how to use the available tools, data, dimensions, and metrics)\<br/>• `SEGMENT_DEFINITION_GUIDE` (segment definition and body structure)\<br/>• `CALCULATED_METRIC_DEFINITION_GUIDE` (calculated metric definition and body structure)\<br/>• `IMS_ORG_CONTEXT_GUIDE` (IMS Org context)\<br/>• `REPORT_SUITE_CONTEXT_GUIDE` (report suite context)\<br/>• `PROJECT_BASE` (required first for project work; project structure, entities, date ranges, hierarchy, troubleshooting)\<br/>• `PROJECT_DATE_RANGES` (advanced date formulas, day-of-week filters, date comparison columns)\<br/>• `PROJECT_PANELS` (layout, dropdown filters, grid layouts, Quick Insights, Next/Previous Item)\<br/>• `PROJECT_FREEFORM_TABLE` (tables, columns, breakdowns, static rows, multi-dimension)\<br/>• `PROJECT_VISUALIZATIONS` (viz type index, linking charts to tables, lockedSelection)\<br/>• `PROJECT_VIZ_BAR`\<br/>• `PROJECT_VIZ_AREA`\<br/>• `PROJECT_VIZ_SCATTER`\<br/>• `PROJECT_VIZ_BULLET`\<br/>• `PROJECT_VIZ_SUMMARY_CHANGE`\<br/>• `PROJECT_VIZ_SECTION_HEADER`\<br/>• `PROJECT_VIZ_TEXT`\<br/>• `PROJECT_VIZ_FALLOUT`\<br/>• `PROJECT_VIZ_FLOW`\<br/>• `PROJECT_VIZ_COMBO`\<br/>• `PROJECT_VIZ_COHORT`\<br/>• `PROJECT_VIZ_HISTOGRAM`\<br/>• `PROJECT_VIZ_JOURNEY_CANVAS`\<br/>• `PROJECT_VIZ_KEY_METRIC_SUMMARY`\<br/>• `PROJECT_VIZ_MAP`\<br/>• `PROJECT_VIZ_VENN` |

**Example prompts:**

* "How do I use the Adobe Analytics tools?"
* "Show me the segment definition guide."
* "How do I create a calculated metric?"
* "What dimensions and metrics are available in my report suite?"
* "Summarize my report suite, including its most-used dimensions, metrics, and segments."
* "How do I structure a workspace project definition?"
* "Show me how to create a flow visualization in a project."
* "What's the JSON structure for a freeform table in a workspace project?"
* "Show me the guide for cohort visualizations."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Set Session Defaults (`setSessionDefaults`)

Sets the default report suite ID and global company ID for the current session. Once set, other tools that accept `globalCompanyId` and `reportSuiteId` parameters can omit them and the server automatically uses these defaults. Both parameters are independently settable. The defaults persist for up to 8 hours.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `reportSuiteId` | No | String | The report suite ID to set as the session default (for example, `examplersid`). |
| `globalCompanyId` | No | String | The global company ID to set as the session default (for example, `analyt6`). |

**Example prompts:**

* "Set my default report suite to examplersid."
* "Set my global company ID to analyt6."
* "Use report suite 'myrsid' and company 'mycompany' for all my queries."
* "Switch to a different report suite."

<AccordionItem slots="heading, text, text, text, text, text"/>

### Get Default Report Suite (`getDefaultSessionReportSuiteId`)

Returns the current default report suite ID for this session. Returns "(not set)" if no default has been configured. Use this tool to confirm which report suite is currently active before running queries.

**Parameters:**

This tool does not require any parameters.

**Example prompts:**

* "What is my current default report suite?"
* "Which report suite am I using?"
* "Show me my session defaults."

<AccordionItem slots="heading, text, text, text, text, text"/>

### Clear Default Report Suite (`clearDefaultSessionReportSuiteId`)

Clears the default report suite ID for this session. After clearing, tools that require a report suite ID will need it provided explicitly again.

**Parameters:**

This tool does not require any parameters.

**Example prompts:**

* "Clear my default report suite."
* "Reset my report suite setting."
* "Remove the default report suite."

## Discovery

<AccordionItem slots="heading, text, text, text, text, text"/>

### Find Companies (`findCompanies`)

Lists all companies (login companies) accessible to the current user. Use this tool to discover which companies you have access to and to obtain a `globalCompanyId` for use with other tools or to set as a session default with `setSessionDefaults`.

**Parameters:**

This tool does not require any parameters.

**Example prompts:**

* "What companies do I have access to?"
* "List my available companies."
* "Show me my login companies."
* "What is my global company ID?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Report Suites (`findReportSuites`)

Finds report suites accessible to the user within a specific company. Returns a paginated list, useful for discovering available report suites or obtaining a report suite ID to set as the session default with `setSessionDefaults`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | Yes | String | The global company ID. |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of report suites to return per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `name`: Includes the display name of the report suite.\<br/>• `description`: Includes the description of the report suite. |

**Example prompts:**

* "What report suites are available?"
* "List my report suites."
* "Show me all report suites in my company."
* "Which report suites do I have access to?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Dimensions (`findDimensions`)

Finds dimensions available to the user for the given report suite. Use this tool to discover which dimensions exist before running a report, or to browse available dimensions. Hidden dimensions are excluded by default. Results are sorted by relevancy based on your personal and organization usage history. The returned dimension IDs can be used directly in `runReport` and `searchDimensionItems`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `page` | Yes | Integer | Page number for pagination (starts at 1). |
| `limit` | Yes | Integer | Number of dimensions to return per page (default 500, max 1000). |
| `includeHidden` | No | Boolean | Include dimensions marked as hidden. Defaults to `false`. |

**Example prompts:**

* "What dimensions are available in my report suite?"
* "List all dimensions."
* "Show me the first page of dimensions."
* "Find dimensions including hidden ones."

<AccordionItem slots="heading, text, text, text, table, text, text"/>

### Find Metrics (`findMetrics`)

Finds available metrics for the given report suite. Use this tool to discover which metrics exist before building a report. Hidden metrics are excluded by default. Results are sorted by relevancy based on your personal and organization usage history. This tool returns both standard metrics and calculated metrics in a single response.

* When a user asks for "metrics", return only standard metrics.
* When a user specifically mentions "calculated metrics", return only calculated metrics.
* When a user asks for "any" or "all" metrics, return everything including calculated metrics.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `page` | No | Integer | Page number for pagination (starts at 0). |
| `limit` | No | Integer | Number of metrics per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the metric was last modified.\<br/>• `componentType`: Adds a string field identifying the component type (for example, `metric`). Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the metric, such as issues with the definition or compatibility problems.\<br/>• `hidden`: Adds a boolean indicating whether the metric is hidden from the default UI view. Hidden metrics are excluded from normal listings but can still be used in reports.\<br/>• `dataName`: Includes the name of the report suite that the metric belongs to. Useful for identifying the data source when working across multiple report suites.\<br/>• `categories`: Adds product category classification information, providing a higher-level organizational grouping for the metric. |
| `includeHidden` | No | Boolean | Include metrics marked as hidden. Defaults to `false`. |
| `includeType` | No | String | Include additional metrics not owned by the current user. Use `all` to return all metrics in the organization (requires Adobe Analytics product admin privileges). If omitted, returns metrics visible to the current user. |

**Example prompts:**

* "What metrics are available in my report suite?"
* "Find all metrics including calculated metrics."
* "Show me available metrics with their tags."
* "List all metrics including hidden ones."
* "What calculated metrics exist?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Segments (`findSegments`)

Finds segments available to the user. Returns a paginated list of segments that the current user has access to. Useful for discovering segments to apply as filters in `runReport` or for retrieving a segment ID to pass to `describeSegment`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of segments per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `dataId`: Includes the associated report suite ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the segment. Useful for identifying the data source when working across multiple report suites.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization. |
| `includeType` | No | String | Include additional segments not owned by the current user. Use `all` to return all segments in the organization (requires Adobe Analytics product admin privileges). If omitted, returns segments visible to the current user. |

**Example prompts:**

* "What segments are available?"
* "Show me the list of segments."
* "List all segments with their tags."
* "Find segments in my organization."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Date Ranges (`findDateRanges`)

Finds saved date range components available to the user. Returns a paginated list, useful for discovering reusable date ranges or retrieving a date range ID for use in a project definition.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of date ranges per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the date range owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the date range was last modified.\<br/>• `definition`: Includes the full date range definition as a JSON object, describing the start and end dates or relative date formula.\<br/>• `tags`: Includes an array of tag objects associated with the date range, each containing the tag ID, name, and other metadata for organizational categorization. |
| `includeType` | No | String | Include additional date ranges not owned by the current user. Use `all` to return all date ranges in the organization (requires Adobe Analytics product admin privileges). If omitted, returns date ranges visible to the current user. |

**Example prompts:**

* "What date ranges are available?"
* "Show me saved date ranges."
* "List all date range components."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Projects (`findProjects`)

Finds workspace projects available to the user. Returns a paginated list, useful for discovering existing projects or obtaining a project ID for use with `describeProject` or `upsertProject`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of projects per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `dataId`: Includes the associated report suite ID that the project is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the project. Useful for identifying the data source when working across multiple report suites.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `definition`: Includes the full project definition as a JSON object, describing the panels, visualizations, freeform tables, and other components that make up the workspace project.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |
| `includeType` | No | String | Include additional projects not owned by the current user. Use `all` to return all projects in the organization (requires Adobe Analytics product admin privileges). If omitted, returns projects visible to the current user. |

**Example prompts:**

* "What workspace projects do I have?"
* "List all projects."
* "Show me my projects."
* "Find projects in my organization."

## Reporting and analysis

<AccordionItem slots="heading, text, text, table, text, text"/>

### Run Report (`runReport`)

The primary tool for pulling analytics data from Adobe Analytics. Runs a ranked report with one dimension and one or more metrics over a specified date range. Metrics are assigned column IDs starting from `0` in the order provided. Results are sorted by the first metric in descending order by default. Segments can be applied as global filters (AND'd together). An optional `allocationModel` parameter lets you apply an attribution model to each metric.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `dimensionId` | Yes | String | The ID of the dimension to analyze in the report (for example, `variables/daterangeday`). |
| `metricIds` | Yes | String | The ID(s) of the metric(s) to measure. For a single metric, provide one ID (for example, `metrics/occurrences`). For multiple, provide comma-separated IDs (for example, `metrics/occurrences,metrics/pageviews`). |
| `startDate` | Yes | String | Start date for the report period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `endDate` | Yes | String | End date for the report period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `segmentIds` | No | String | The ID(s) of the segment(s) to apply as global filters. For a single segment, provide one ID. For multiple, provide comma-separated IDs. Each segment is applied as a global filter (AND'd). |
| `limit` | No | Integer | Number of rows to return (default 100, max 1000). |
| `allocationModel` | No | String (enum) | The attribution model applied to each metric. Only valid on standard metrics, not calculated metrics. Supported values include:\<br/>• `lastTouch`\<br/>• `firstTouch`\<br/>• `linear`\<br/>• `participation`\<br/>• `uShaped`\<br/>• `jShaped`\<br/>• `reverseJShaped`\<br/>• `positionBased`\<br/>• `timeDecay`\<br/>• `algorithmic`\<br/>• `instance` |

**Example prompts:**

* "Show me page views by day for the last 30 days."
* "Run a report of the top pages by visits for March 2025."
* "What are the top 10 marketing channels by revenue this quarter?"
* "Run a report with occurrences and page views by page for last week."
* "Show me visits by browser using first touch attribution."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Search Dimension Items (`searchDimensionItems`)

Retrieves the top dimension items for a given dimension. For example, if the dimension is "Country", this tool returns items like US, UK, Canada, etc. Also supports keyword search to find specific items within a dimension.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `dimensionId` | Yes | String | The ID of the dimension to analyze (for example, `variables/daterangeday`). The `variables/` prefix is required. |
| `startDate` | Yes | String | Start of the reporting period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `endDate` | Yes | String | End date in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `page` | Yes | Integer | Page number for pagination (starts at 1). |
| `limit` | Yes | Integer | Number of dimension items per page (max 1000). |
| `searchAnd` | No | String | Search terms that are AND'd together. Space delimited. |
| `searchOr` | No | String | Search terms that are OR'd together. Space delimited. |

**Example prompts:**

* "What are the top countries by traffic this month?"
* "Show me all the page names for last week."
* "Search for dimension items containing 'checkout' in the page dimension."
* "What values does the marketing channel dimension have?"
* "Get the top browsers in the last 30 days."

## Component details

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Segment (`describeSegment`)

Returns metadata for a given segment, including its name, description, definition, and compatibility. Use this tool to understand what a segment filters for, to inspect its definition before modifying it with `upsertSegment`, or to check its compatibility.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `segmentId` | Yes | String | The segment ID. |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `isDeleted`: Adds a boolean indicating whether the segment has been deleted.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `definition`: Includes the full segment definition as a JSON object, describing the container structure and predicates that define the segment logic.\<br/>• `internal`: Adds a boolean indicating whether this is an internal system segment not normally visible to users.\<br/>• `definitionLastModified`: Adds an ISO 8601 timestamp showing when the segment definition was last modified, independent of metadata changes.\<br/>• `createdDate`: Adds an ISO 8601 timestamp showing when the segment was originally created.\<br/>• `dataId`: Includes the associated report suite ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the segment. Useful for identifying the data source when working across multiple report suites.\<br/>• `owner`: Includes the segment owner object containing the user ID.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `usageSummary`: Includes a summary of where and how often the segment is used across projects and reports in the organization. |

**Example prompts:**

* "Describe segment s12345."
* "Show me the definition of the 'Mobile Users' segment."
* "What does this segment filter for?"
* "Get the details of my segment including its definition."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Calculated Metric (`describeCalculatedMetric`)

Shows the metric formula and base metrics used for a calculated metric. Use this tool to understand how a calculated metric is constructed, which base metrics it depends on, or to inspect it before modifying it with `upsertCalculatedMetric`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `id` | Yes | String | The calculated metric ID. |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the calculated metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the calculated metric was last modified.\<br/>• `definition`: Includes the full calculated metric definition as a JSON object, describing the formula structure and base metrics used.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the calculated metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the calculated metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the calculated metric, such as issues with the definition or compatibility problems.\<br/>• `compatibility`: Adds information about which products the calculated metric is compatible with.\<br/>• `hidden`: Adds a boolean indicating whether the calculated metric is hidden from the default UI view.\<br/>• `dataName`: Includes the name of the report suite associated with the calculated metric. Useful for identifying the data source when working across multiple report suites. |

**Example prompts:**

* "Show me the formula for calculated metric cm12345."
* "How is this calculated metric defined?"
* "What base metrics does this calculated metric use?"
* "Describe the 'Conversion Rate' calculated metric."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Project (`describeProject`)

Shows details about a workspace project, including its name, description, owner, and report suite. The response automatically includes a `workspaceLink` field with a direct URL to open the project in Analysis Workspace. Use this tool to inspect a project's configuration, retrieve its full definition before modifying it with `upsertProject`, or determine which report suite it uses.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `id` | Yes | String | The project ID. |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `dataId`: Includes the associated report suite ID that the project is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the project. Useful for identifying the data source when working across multiple report suites.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `definition`: Includes the full project definition as a JSON object, describing the panels, visualizations, freeform tables, and other components that make up the workspace project.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |

**Example prompts:**

* "Describe project proj12345."
* "Show me the details of the 'Marketing Dashboard' project."
* "What report suite does this project use?"
* "Get the full definition of my workspace project."

## Component usage

<AccordionItem slots="heading, text, text, table, text, text"/>

### List Component Usage (`listComponentUsage`)

Lists the components of a specified type that are most used in reports, ranked by usage frequency. Use this tool to discover which dimensions, metrics, segments, or other components are most popular in your organization. Helpful when deciding what to include in a new report or project.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `componentType` | Yes | String | The type of component to check. Available types include:\<br/>• `dimension`\<br/>• `metric`\<br/>• `segment`\<br/>• `dateRange`\<br/>• `project`\<br/>• `calculatedMetric` |

**Example prompts:**

* "What are the most used dimensions in reports?"
* "Show me the most popular metrics."
* "Which segments are used the most?"
* "What are the top components by usage?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### List Frequently Used With (`listFrequentlyUsedWith`)

Lists components that are frequently used together in reports with a specified component. Use this tool to discover natural pairings to inform report building. For example, use this tool to determine which metrics are commonly used alongside a specific dimension.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `componentId` | Yes | String | The ID of the component to check. |
| `componentType` | Yes | String | The type of the component. Available types include:\<br/>• `dimension`\<br/>• `metric`\<br/>• `segment`\<br/>• `dateRange`\<br/>• `project`\<br/>• `calculatedMetric` |

**Example prompts:**

* "What components are frequently used with the 'page' dimension?"
* "What metrics are commonly paired with the 'marketing channel' dimension?"
* "Show me what's frequently used alongside the 'visits' metric."
* "What else is typically used with this segment?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### List Similar Components (`listSimilarTo`)

Lists components that are similar to a specified component. Use this tool to find alternatives or related dimensions, metrics, or segments that serve a similar purpose.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `componentId` | Yes | String | The ID of the component to check. |
| `componentType` | Yes | String | The type of the component. Available types include:\<br/>• `dimension`\<br/>• `metric`\<br/>• `segment`\<br/>• `dateRange`\<br/>• `project`\<br/>• `calculatedMetric` |

**Example prompts:**

* "What dimensions are similar to 'page'?"
* "Find metrics similar to 'visits'."
* "Show me segments similar to this one."
* "What alternatives exist for this dimension?"

## Create and update

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Segment (`upsertSegment`)

Creates a new segment or updates an existing one. If a `segmentId` is provided, updates the existing segment; if omitted, creates a new one. Before calling this tool, call `describeAa(SEGMENT_DEFINITION_GUIDE)` to learn the required segment body structure.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `segmentId` | No | String | The ID of the segment to update. If not provided, creates a new segment instead. |
| `segmentBody` | Yes | Object | The segment metadata and definition object. Includes fields such as `name`, `description`, `definition` (container structure with predicates), and `compatibility`. Call `describeAa(SEGMENT_DEFINITION_GUIDE)` for the full structure. |
| `expansions` | No | String | Additional data to return on the created or updated segment. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `definition`: Includes the full segment definition as a JSON object, describing the container structure and predicates that define the segment logic.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `dataId`: Includes the associated report suite ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the segment. Useful for identifying the data source when working across multiple report suites.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization. |

**Example prompts:**

* "Create a segment for mobile users."
* "Create a segment that filters for visitors from the United States."
* "Update the definition of segment s12345."
* "Build a segment for users who visited the checkout page."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Calculated Metric (`upsertCalculatedMetric`)

Creates a new calculated metric or updates an existing one. If a `calculatedMetricId` is provided, updates the existing calculated metric; if omitted, creates a new one. Before calling this tool, call `describeAa(CALCULATED_METRIC_DEFINITION_GUIDE)` to learn the required metric body structure.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `calculatedMetricId` | No | String | The ID of the calculated metric to update. If not provided, creates a new calculated metric instead. |
| `metricBody` | Yes | Object | The metric metadata and definition object. Includes fields such as `name`, `description`, `dataId` (the report suite ID), and `definition` (formula structure). Call `describeAa(CALCULATED_METRIC_DEFINITION_GUIDE)` for the full structure. |
| `expansions` | No | String | Additional data to return on the created or updated calculated metric. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the calculated metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the calculated metric was last modified.\<br/>• `definition`: Includes the full calculated metric definition as a JSON object, describing the formula structure and base metrics used.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the calculated metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the calculated metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the calculated metric, such as issues with the definition or compatibility problems.\<br/>• `compatibility`: Adds information about which products the calculated metric is compatible with.\<br/>• `hidden`: Adds a boolean indicating whether the calculated metric is hidden from the default UI view.\<br/>• `dataName`: Includes the name of the report suite associated with the calculated metric. Useful for identifying the data source when working across multiple report suites. |

**Example prompts:**

* "Create a calculated metric for conversion rate (orders divided by visits)."
* "Build a calculated metric that divides revenue by visitors."
* "Update calculated metric cm12345 with a new formula."
* "Create a bounce rate calculated metric."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create Date Range (`createDateRange`)

Creates a new reusable date range component that can be shared and used across projects.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `dateRangeBody` | Yes | Object | The date range definition as a map. See the API documentation for the required structure. |
| `expansions` | No | String | Additional data to return on the created date range. Available expansions:\<br/>• `definition`: Includes the full date range definition as a JSON object, describing the start and end dates or relative date formula.\<br/>• `ownerFullName`: Includes the full name and login of the date range owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the date range was last modified.\<br/>• `approved`: Adds a boolean indicating whether the date range has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the date range, each containing the tag ID, name, and other metadata for organizational categorization. |

**Example prompts:**

* "Create a date range for Q1 2025."
* "Build a date range component for the last 90 days."
* "Create a custom date range from January 1 to March 31."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Project (`upsertProject`)

Creates a new workspace project or updates an existing one. If a `projectId` is provided, updates the existing project; if omitted, creates a new one. Before calling this tool, call `describeAa(PROJECT_BASE)` to learn the required project structure. For specific visualization types, also call `describeAa` with the appropriate guide type (for example, `PROJECT_VIZ_COMBO`, `PROJECT_VIZ_FLOW`, `PROJECT_FREEFORM_TABLE`). The `projectBody` must include `dataId` set to the report suite ID (same value as `rsid` and panel `reportSuite.id`); omitting `dataId` commonly causes "referenced component was not found in this report suite" errors. The response automatically includes a `workspaceLink` field with a direct URL to open the project in Analysis Workspace.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `globalCompanyId` | No | String | The global company ID. If omitted, uses the session default. |
| `reportSuiteId` | No | String | The report suite ID. If omitted, uses the session default. |
| `projectId` | No | String | The ID of the project to update. If not provided, creates a new project instead. |
| `projectBody` | Yes | Object | The project payload including `definition`, `dataId` (must be set to the report suite ID), `type` (must be `project`), and optionally `name` and `description`. Call `describeAa(PROJECT_BASE)` for the full structure. |
| `expansions` | No | String | Additional data to return on the created or updated project. Available expansions:\<br/>• `dataId`: Includes the associated report suite ID that the project is tied to.\<br/>• `dataName`: Includes the name of the report suite associated with the project. Useful for identifying the data source when working across multiple report suites.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `definition`: Includes the full project definition as a JSON object, describing the panels, visualizations, freeform tables, and other components that make up the workspace project.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |

**Example prompts:**

* "Create a new workspace project with a freeform table showing page views by day."
* "Build a project with a bar chart of top pages by visits."
* "Update project proj12345 to add a new panel."
* "Create a workspace project with a flow visualization."
* "Build a marketing dashboard project."
