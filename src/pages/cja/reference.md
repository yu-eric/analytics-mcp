---
title: Customer Journey Analytics MCP server tool reference
description: A complete reference of all tools available in the Customer Journey Analytics MCP server, including descriptions, parameters, and usage details.
---

# Customer Journey Analytics MCP server tool reference

The following tools are available when connected to the Customer Journey Analytics MCP server. Each tool can be invoked by an LLM client to interact with your Customer Journey Analytics data, components, and workspace projects.

## Setup and guides

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Customer Journey Analytics (`describeCja`)

The starting point for learning how to use the Customer Journey Analytics MCP tools. Returns focused reference guides covering tool usage, available dimensions and metrics, segment definition syntax, calculated metric definition syntax, the two-step breakdown report workflow, and workspace project definitions. Call this tool before creating segments, calculated metrics, breakdown reports, or workspace projects to learn the required structures.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `guideType` | No | String (enum) | The type of guide to return. Defaults to `CJA_REFERENCE_GUIDE` if omitted. Valid values include:\<br/>• `CJA_REFERENCE_GUIDE` (how to use the available tools, data, dimensions, and metrics)\<br/>• `SEGMENT_DEFINITION_GUIDE` (segment definition and body structure)\<br/>• `CALCULATED_METRIC_DEFINITION_GUIDE` (calculated metric definition and body structure)\<br/>• `BREAKDOWN_GUIDE` (how to run breakdown reports and the required two-step workflow)\<br/>• `IMS_ORG_CONTEXT_GUIDE` (IMS Org context)\<br/>• `DATAVIEW_CONTEXT_GUIDE` (data view context)\<br/>• `PROJECT_BASE` (required first for project work; project structure, entities, date ranges, hierarchy, troubleshooting)\<br/>• `PROJECT_DATE_RANGES` (advanced date formulas, day-of-week filters, date comparison columns)\<br/>• `PROJECT_PANELS` (layout, dropdown filters, grid layouts, Quick Insights, Next/Previous Item)\<br/>• `PROJECT_FREEFORM_TABLE` (tables, columns, breakdowns, static rows, multi-dimension)\<br/>• `PROJECT_VISUALIZATIONS` (viz type index, linking charts to tables, lockedSelection)\<br/>• `PROJECT_VIZ_BAR`\<br/>• `PROJECT_VIZ_AREA`\<br/>• `PROJECT_VIZ_SCATTER`\<br/>• `PROJECT_VIZ_BULLET`\<br/>• `PROJECT_VIZ_SUMMARY_CHANGE`\<br/>• `PROJECT_VIZ_SECTION_HEADER`\<br/>• `PROJECT_VIZ_TEXT`\<br/>• `PROJECT_VIZ_FALLOUT`\<br/>• `PROJECT_VIZ_FLOW`\<br/>• `PROJECT_VIZ_COMBO`\<br/>• `PROJECT_VIZ_COHORT`\<br/>• `PROJECT_VIZ_HISTOGRAM`\<br/>• `PROJECT_VIZ_JOURNEY_CANVAS`\<br/>• `PROJECT_VIZ_KEY_METRIC_SUMMARY`\<br/>• `PROJECT_VIZ_MAP`\<br/>• `PROJECT_VIZ_VENN` |
| `dataViewId` | No | String | Override data view ID. Provide this parameter when calling with `DATAVIEW_CONTEXT_GUIDE`. |

**Example prompts:**

* "How do I use the Customer Journey Analytics tools?"
* "Show me the segment definition guide."
* "How do I create a calculated metric?"
* "How do breakdown reports work?"
* "What dimensions and metrics are available in my data view?"
* "How do I structure a workspace project definition?"
* "Show me how to create a flow visualization in a project."
* "What's the JSON structure for a freeform table in a workspace project?"
* "Show me the guide for cohort visualizations."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Set Default Data View (`setDefaultSessionDataViewId`)

Sets the default data view ID for the current session. Once set, other tools that accept a `dataViewId` parameter can omit it and the server automatically uses this data view. This tool is useful when working within a single data view across multiple tool calls, or when switching the active data view for your session. The default persists for up to 8 hours.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | Yes | String | The data view ID to set as the session default (for example, `dv_62ba17d5a5d7845496f5fb4d`). |

**Example prompts:**

* "Set my default data view to dv_62ba17d5a5d7845496f5fb4d."
* "Use the 'Production Web' data view for all my queries."
* "Switch to a different data view."

## Discovery

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Dimensions (`findDimensions`)

Finds dimensions available in a given data view. Use this tool to discover which dimensions exist before running a report, or to find dimensions related to a specific topic. Supports semantic search; pass a `searchQuery` with a topic or purpose (for example, "date time", "page", "user") to get relevance-ranked results. When `searchQuery` is omitted, returns a full paginated list sorted by relevancy based on your personal and organization usage history. Hidden dimensions are excluded by default. The returned dimension IDs can be used directly in `runReport` and `searchDimensionItems`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `searchQuery` | No | String | Semantic search query (topic, name, or purpose). Returns relevance-ranked results when provided. Recommended for discovery. |
| `page` | No | Integer | Page number for pagination (starts at 1). Only used when `searchQuery` is not provided. |
| `limit` | No | Integer | Number of dimensions per page (default 500, max 1000). Only used when `searchQuery` is not provided. |
| `includeHidden` | No | Boolean | Include dimensions marked as hidden. Defaults to `false`. |

**Example prompts:**

* "What dimensions are available in my data view?"
* "Find dimensions related to marketing channels."
* "Search for date-related dimensions."
* "Show me all page-related dimensions."
* "List all dimensions in my data view."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Metrics (`findMetrics`)

Finds available standard and custom metrics from the data view. Use this tool to discover which metrics exist before building a report, or to find metrics related to a specific topic (for example, "revenue", "engagement"). Does NOT include calculated metrics; use `findCalculatedMetrics` for those. Supports semantic search; pass a `searchQuery` to get relevance-ranked results. When `searchQuery` is omitted, the tool returns a full paginated list sorted by relevancy based on your personal and organization usage history. Hidden metrics are excluded by default.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `searchQuery` | No | String | Semantic search query (topic, name, or purpose). Returns relevance-ranked results when provided. Recommended for discovery. |
| `page` | No | Integer | Page number for pagination (starts at 1). Only used when `searchQuery` is not provided. |
| `limit` | No | Integer | Number of metrics per page (default 100, max 1000). Only used when `searchQuery` is not provided. |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the metric was last modified.\<br/>• `componentType`: Adds a string field identifying the component type (for example, `metric`). Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `hidden`: Adds a boolean indicating whether the metric is hidden from the default UI view. Hidden metrics are excluded from normal listings but can still be used in reports.\<br/>• `dataName`: Includes the name of the data view that the metric belongs to. Useful for identifying the data source when working across multiple data views.\<br/>• `categories`: Adds product category classification information, providing a higher-level organizational grouping for the metric. |
| `includeHidden` | No | Boolean | Include metrics marked as hidden. Defaults to `false`. |

**Example prompts:**

* "What metrics are available in my data view?"
* "Find metrics related to revenue."
* "Search for conversion-related metrics."
* "Show me all session and visit metrics."
* "List available metrics."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Calculated Metrics (`findCalculatedMetrics`)

Finds available calculated metrics. Use this tool when specifically looking for calculated metrics rather than standard metrics (use `findMetrics` for those). Useful for browsing or searching user-created and shared calculated metrics. Hidden calculated metrics are excluded by default. Pagination is applied by the downstream API before hidden filtering, so filtered pages can return fewer than `limit` results.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `page` | No | Integer | Page number for pagination (starts at 0). |
| `limit` | No | Integer | Number of results per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the calculated metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the calculated metric was last modified.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the calculated metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the calculated metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the calculated metric, such as issues with the definition or compatibility problems.\<br/>• `hidden`: Adds a boolean indicating whether the calculated metric is hidden from the default UI view.\<br/>• `dataName`: Includes the name of the data view associated with the calculated metric. Useful for identifying the data source when working across multiple data views.\<br/>• `categories`: Adds product category classification information, providing a higher-level organizational grouping for the calculated metric. |
| `includeType` | No | String | Include additional calculated metrics not owned by the current user. The `all` option takes precedence over `shared`. Available values:\<br/>• `all`: Returns all calculated metrics in the organization (requires product admin privileges).\<br/>• `shared`: Includes calculated metrics that have been shared with the current user by other users.\<br/>• `templates`: Includes template calculated metrics provided by the system.\<br/>• `deleted`: Includes calculated metrics that have been deleted.\<br/>• `internal`: Includes internal system calculated metrics not normally visible to users.\<br/>• `curatedItem`: Includes curated calculated metrics.\<br/>If omitted, returns only calculated metrics visible to the current user. |
| `includeHidden` | No | Boolean | Include calculated metrics marked as hidden. Defaults to `false`. |

**Example prompts:**

* "Show me the available calculated metrics."
* "What calculated metrics exist in my organization?"
* "List all calculated metrics, including hidden ones."
* "Find calculated metrics with their tags."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Segments (`findSegments`)

Finds segments available to the user. Returns a paginated list of segments that the current user has access to. Useful for discovering segments to apply as filters in `runReport` or for retrieving a segment ID to pass to `describeSegment`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of segments per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `dataId`: Includes the associated data view ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the segment. Useful for identifying the data source when working across multiple data views.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization. |
| `includeType` | No | String | Include additional segments not owned by the current user. Available values:\<br/>• `all`: Returns all components in the organization, including shared, templates, deleted, and internal (requires product admin privileges).\<br/>• `shared`: Includes segments that have been shared with the current user by other users.\<br/>• `templates`: Includes template segments provided by the system.\<br/>• `deleted`: Includes segments that have been deleted. Deleted segments are only returned when explicitly requested.\<br/>• `internal`: Includes internal system segments not normally visible to users.\<br/>If omitted, returns only segments owned by the current user. |

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
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of date ranges per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the date range owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the date range was last modified.\<br/>• `definition`: Includes the full date range definition as a JSON object, describing the start and end dates or relative date formula.\<br/>• `tags`: Includes an array of tag objects associated with the date range, each containing the tag ID, name, and other metadata for organizational categorization. |
| `includeType` | No | String | Include additional date ranges not owned by the current user. Available values:\<br/>• `all`: Returns all date ranges in the organization, including shared and templates (requires product admin privileges).\<br/>• `shared`: Includes date ranges that have been shared with the current user by other users.\<br/>• `templates`: Includes template date ranges provided by the system.\<br/>If omitted, returns only date ranges owned by the current user. |

**Example prompts:**

* "What date ranges are available?"
* "Show me saved date ranges."
* "List all date range components."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Data Views (`findDataViews`)

Finds data views accessible to the user. Returns a paginated list, useful for discovering available data views or obtaining a data view ID to set as the session default with `setDefaultSessionDataViewId`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of data views per page (max 1000). |
| `expansions` | No | String | Additional data to return. Available expansions:\<br/>• `name`: Includes the display name of the data view.\<br/>• `description`: Includes the description of the data view. |
| `includeType` | No | String | Include additional data views not owned by the current user. Available values:\<br/>• `all`: Returns all data views in the organization (requires product admin privileges).\<br/>If omitted, returns only data views visible to the current user. |

**Example prompts:**

* "What data views are available?"
* "List my data views."
* "Show me all data views in my organization."
* "Which data views do I have access to?"

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Projects (`findProjects`)

Finds workspace projects available to the user. Returns a paginated list, useful for discovering existing projects or obtaining a project ID for use with `describeProject` or `upsertProject`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of projects per page (max 1000). |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `dataId`: Includes the associated data view ID that the project is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the project. Useful for identifying the data source when working across multiple data views.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |
| `includeType` | No | String | Include additional projects not owned by the current user. Available values:\<br/>• `all`: Returns all projects in the organization (requires product admin privileges).\<br/>• `shared`: Includes projects that have been shared with the current user by other users.\<br/>If omitted, returns only projects owned by the current user. |

**Example prompts:**

* "What workspace projects do I have?"
* "List all projects."
* "Show me my projects."
* "Find projects in my organization."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Find Audiences (`findAudiences`)

Lists audiences available to the user. Returns a paginated list of audience components, useful for discovering existing audiences or obtaining an audience ID for use with `describeAudience` or `upsertAudience`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `page` | No | Integer | Page number for pagination (starts at 0). |
| `limit` | No | Integer | Number of audiences per page (max 1000). |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `name`: Includes the display name of the audience.\<br/>• `description`: Includes the description of the audience.\<br/>• `ownerFullName`: Includes the full name and login of the audience owner, expanding the `owner` object beyond just the user ID.\<br/>• `frequency`: Includes the refresh frequency configuration for the audience, indicating how often the audience membership is recalculated.\<br/>• `expirationDate`: Includes the expiration date after which the audience is no longer active or published.\<br/>• `publishingStatus`: Includes the current publishing status of the audience (for example, whether it is actively being published to a destination).\<br/>• `dataViewId`: Includes the data view ID that the audience is associated with.\<br/>• `modifiedDate`: Adds an ISO 8601 timestamp showing when the audience was last modified.\<br/>• `createdDate`: Adds an ISO 8601 timestamp showing when the audience was originally created.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the audience has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the audience, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `size`: Includes the current estimated size (member count) of the audience. |
| `includeType` | No | String | Include additional audiences not owned by the current user. Available values:\<br/>• `all`: Returns all audiences in the organization (requires product admin privileges).\<br/>If omitted, returns only audiences visible to the current user. |

**Example prompts:**

* "What audiences are available?"
* "List my audiences."
* "Show me all audiences in my organization."

## Reporting and analysis

<AccordionItem slots="heading, text, text, table, text, text"/>

### Run Report (`runReport`)

The primary tool for pulling analytics data from Customer Journey Analytics. Runs a ranked report with support for single or multiple dimensions and metrics over a specified date range. All dimensions and metrics are reported together in a single request. Dimensions are assigned column IDs starting from `0` in the order provided. Metrics are also assigned column IDs starting from `0`. Results are sorted by the first metric in descending order by default. Segments can be applied as global filters, and breakdown reports are supported via the optional `breakdowns` parameter — call `describeCja(BREAKDOWN_GUIDE)` for the full two-step workflow.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `dimensionIds` | Yes | String | The ID(s) of the dimension(s). For a single dimension, provide one ID (for example, `variables/daterangeday`). For multiple, provide comma-separated IDs (for example, `variables/daterangeday,variables/page`). Each dimension is assigned a column ID starting from `0`. |
| `metricIds` | Yes | String | The ID(s) of the metric(s). For a single metric, provide one ID (for example, `metrics/occurrences`). For multiple, provide comma-separated IDs (for example, `metrics/occurrences,metrics/visits,metrics/visitors`). Each metric is assigned a column ID starting from `0`. |
| `startDate` | Yes | String | Start date for the report period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `endDate` | Yes | String | End date for the report period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | No | Integer | Number of dimension items per page (max 1000). Defaults to 100 if not specified. |
| `segmentIds` | No | String | The ID(s) of segments to apply as global filters. For a single segment, provide one ID (for example, `s123`). For multiple, provide comma-separated IDs (for example, `s123,s456`). |
| `adhocSegments` | No | List | One or more ad hoc segment definitions to apply as global filters. Provide a list of segment definition objects. Each definition is applied as a separate global filter (AND'd together). Cannot be used together with `segmentIds`. |
| `sort` | No | List | Sort settings for the report. Each entry is an object with\<br/>• `componentType` (`metric` or `dimension`)\<br/>• `columnId` (optional — the column to sort by, for example, `0` for first, `1` for second. If omitted, the column ID is inferred from the order of sort entries.)\<br/>• `ascending` (boolean)\<br/>Defaults to first metric descending if not provided. |
| `generateRequestOnly` | No | Boolean | When `true`, returns the API request payload without executing the report. Useful for debugging. Defaults to `false`. |
| `breakdowns` | No | List | One or more breakdown filters to scope the report to specific dimension items. Each entry must have `dimensionId` (for example, `variables/daterangeyear`) and `itemId` (the numeric item ID from a prior `runReport` or `searchDimensionItems` call, not the plain text value). Multiple entries are AND'd together. Call `describeCja(BREAKDOWN_GUIDE)` for full workflow instructions. |

**Example prompts:**

* "Show me page views by day for the last 30 days."
* "Run a report of the top pages by visits for March 2025."
* "What are the top 10 marketing channels by revenue this quarter?"
* "Break down page views by country for the US in January 2025."
* "Run a report with sessions and visitors by device type for last week."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Search Dimension Items (`searchDimensionItems`)

Retrieves the top dimension items for a given dimension. For example, if the dimension is "Country", this tool returns items like US, UK, Canada, etc. Also supports keyword search to find specific items. This tool is essential for obtaining the numeric `itemId` values needed for breakdown reports in `runReport`.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `dimensionId` | Yes | String | The ID of the dimension to analyze (for example, `variables/daterangeday`). The `variables/` prefix is required. |
| `startDate` | Yes | String | Start of the reporting period in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). You can also provide only the date (`YYYY-MM-DD`), in which case use `00:00:00` as the time. |
| `endDate` | Yes | String | End date in ISO 8601 format (`YYYY-MM-DDTHH:mm:ss`). You can also provide only the date (`YYYY-MM-DD`), in which case use `23:59:59` as the time to include the full day. |
| `page` | Yes | Integer | Page number for pagination (starts at 0). |
| `limit` | Yes | Integer | Number of dimension items per page (max 1000). |
| `searchAnd` | No | String | Search terms that are AND'd together. Space delimited. |
| `searchOr` | No | String | Search terms that are OR'd together. Space delimited. |

**Example prompts:**

* "What are the top countries by traffic this month?"
* "Show me all the page names for last week."
* "Search for dimension items containing 'checkout' in the page dimension."
* "What values does the marketing channel dimension have?"
* "Get the item IDs for the top browsers in the last 30 days."

## Component details

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Dimension (`describeDimension`)

Returns detailed metadata for a given dimension, including its name, description, type, and other properties. Use this tool to understand what a specific dimension represents or to review its metadata before using it in a report.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `dimensionId` | Yes | String | The dimension ID. Remove the `variables/` prefix for this parameter. |

**Example prompts:**

* "What does the 'page' dimension represent?"
* "Describe the 'evar5' dimension."
* "Tell me more about the 'daterangeday' dimension."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Metric (`describeMetric`)

Returns metadata for a given metric, including its name, description, type, and other properties. Use this tool to understand what a specific metric measures or to review its metadata before using it in a report.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
| `metricId` | Yes | String | The metric ID. Remove the `metrics/` prefix for this parameter. |

**Example prompts:**

* "What does the 'occurrences' metric measure?"
* "Describe the 'visits' metric."
* "Tell me about the 'revenue' metric."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Segment (`describeSegment`)

Returns metadata for a given segment, including its name, description, definition, and compatibility. Use this tool to understand what a segment filters for, to inspect its definition before modifying it with `upsertSegment`, or to check its compatibility with a data view.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `segmentId` | Yes | String | The segment ID. |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `definition`: Includes the full segment definition as a JSON object, describing the container structure and predicates that define the segment logic.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `dataId`: Includes the associated data view ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the segment. Useful for identifying the data source when working across multiple data views.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `createdDate`: Adds an ISO 8601 timestamp showing when the segment was originally created. |

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
| `id` | Yes | String | The calculated metric ID. |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the calculated metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the calculated metric was last modified.\<br/>• `definition`: Includes the full calculated metric definition as a JSON object, describing the formula structure and base metrics used.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the calculated metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the calculated metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the calculated metric, such as issues with the definition or compatibility problems.\<br/>• `compatibility`: Adds information about which products the calculated metric is compatible with.\<br/>• `hidden`: Adds a boolean indicating whether the calculated metric is hidden from the default UI view.\<br/>• `dataName`: Includes the name of the data view associated with the calculated metric. Useful for identifying the data source when working across multiple data views.\<br/>• `categories`: Adds product category classification information, providing a higher-level organizational grouping for the calculated metric. |

**Example prompts:**

* "Show me the formula for calculated metric cm12345."
* "How is this calculated metric defined?"
* "What base metrics does this calculated metric use?"
* "Describe the 'Conversion Rate' calculated metric."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Project (`describeProject`)

Shows details about a workspace project, including its name, description, owner, and data view. The response automatically includes a `workspaceLink` field with a direct URL to open the project in Analysis Workspace. Use this tool to inspect a project's configuration, retrieve its full definition before modifying it with `upsertProject`, or determine which data view it uses.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `id` | Yes | String | The project ID. |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `dataId`: Includes the associated data view ID that the project is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the project. Useful for identifying the data source when working across multiple data views.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `definition`: Includes the full project definition as a JSON object, describing the panels, visualizations, freeform tables, and other components that make up the workspace project.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |

**Example prompts:**

* "Describe project proj12345."
* "Show me the details of the 'Marketing Dashboard' project."
* "What data view does this project use?"
* "Get the full definition of my workspace project."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Describe Audience (`describeAudience`)

Returns metadata for a given audience, including its name, description, definition, publishing status, and other properties. Use this tool to understand what an audience targets or to inspect its definition and status.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `audienceId` | Yes | String | The audience ID. |
| `expansions` | Yes | String | Additional data to return. Available expansions:\<br/>• `name`: Includes the display name of the audience.\<br/>• `description`: Includes the description of the audience.\<br/>• `definition`: Includes the full audience definition as a JSON object, describing the segment logic and criteria that determine audience membership.\<br/>• `ownerFullName`: Includes the full name and login of the audience owner, expanding the `owner` object beyond just the user ID.\<br/>• `frequency`: Includes the refresh frequency configuration for the audience, indicating how often the audience membership is recalculated.\<br/>• `expirationDate`: Includes the expiration date after which the audience is no longer active or published.\<br/>• `publishingStatus`: Includes the current publishing status of the audience (for example, whether it is actively being published to a destination).\<br/>• `dataViewId`: Includes the data view ID that the audience is associated with.\<br/>• `modifiedDate`: Adds an ISO 8601 timestamp showing when the audience was last modified.\<br/>• `createdDate`: Adds an ISO 8601 timestamp showing when the audience was originally created.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the audience has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the audience, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `size`: Includes the current estimated size (member count) of the audience. |

**Example prompts:**

* "Describe audience aud12345."
* "What is the definition of this audience?"
* "Show me the publishing status of my audience."

## Component usage

<AccordionItem slots="heading, text, text, table, text, text"/>

### List Component Usage (`listComponentUsage`)

Lists the components of a specified type that are most used in reports, ranked by usage frequency. Use this tool to discover which dimensions, metrics, segments, or other components are most popular in your organization. Helpful when deciding what to include in a new report or project.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
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
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
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
| `dataViewId` | No | String | The data view ID. If omitted, uses the session default. |
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

Creates a new segment or updates an existing one. If a `segmentId` is provided, updates the existing segment; if omitted, creates a new one. Before calling this tool, call `describeCja(SEGMENT_DEFINITION_GUIDE)` to learn the required segment body structure.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `segmentId` | No | String | The ID of the segment to update. If not provided, creates a new segment instead. |
| `segmentBody` | Yes | Object | The segment metadata and definition object. Includes fields such as `name`, `description`, `definition` (container structure with predicates), and `compatibility`. Call `describeCja(SEGMENT_DEFINITION_GUIDE)` for the full structure. |
| `expansions` | Yes | String | Additional data to return on the created or updated segment. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the segment owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the segment was last modified.\<br/>• `definition`: Includes the full segment definition as a JSON object, describing the container structure and predicates that define the segment logic.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the segment is compatible with.\<br/>• `dataId`: Includes the associated data view ID that the segment is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the segment. Useful for identifying the data source when working across multiple data views.\<br/>• `approved`: Adds a boolean indicating whether the segment has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the segment, each containing the tag ID, name, and other metadata for organizational categorization. |

**Example prompts:**

* "Create a segment for mobile users."
* "Create a segment that filters for visitors from the United States."
* "Update the definition of segment s12345."
* "Build a segment for users who visited the checkout page."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Calculated Metric (`upsertCalculatedMetric`)

Creates a new calculated metric or updates an existing one. If a `calculatedMetricId` is provided, updates the existing calculated metric; if omitted, creates a new one. Before calling this tool, call `describeCja(CALCULATED_METRIC_DEFINITION_GUIDE)` to learn the required metric body structure.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `calculatedMetricId` | No | String | The ID of the calculated metric to update. If not provided, creates a new calculated metric instead. |
| `metricBody` | Yes | Object | The metric metadata and definition object. Includes fields such as `name`, `description`, `dataId` (the data view ID), and `definition` (formula structure). Call `describeCja(CALCULATED_METRIC_DEFINITION_GUIDE)` for the full structure. |
| `expansions` | Yes | String | Additional data to return on the created or updated calculated metric. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the calculated metric owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the calculated metric was last modified.\<br/>• `definition`: Includes the full calculated metric definition as a JSON object, describing the formula structure and base metrics used.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the calculated metric has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the calculated metric, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `warning`: Includes any warning messages about the calculated metric, such as issues with the definition or compatibility problems.\<br/>• `compatibility`: Adds information about which products the calculated metric is compatible with.\<br/>• `hidden`: Adds a boolean indicating whether the calculated metric is hidden from the default UI view.\<br/>• `dataName`: Includes the name of the data view associated with the calculated metric. Useful for identifying the data source when working across multiple data views. |

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
| `dateRangeBody` | Yes | Object | The date range definition as a map. See the API documentation for the required structure. |
| `expansions` | Yes | String | Additional data to return on the created date range. Available expansions:\<br/>• `definition`: Includes the full date range definition as a JSON object, describing the start and end dates or relative date formula.\<br/>• `ownerFullName`: Includes the full name and login of the date range owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the date range was last modified.\<br/>• `approved`: Adds a boolean indicating whether the date range has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the date range, each containing the tag ID, name, and other metadata for organizational categorization. |

**Example prompts:**

* "Create a date range for Q1 2025."
* "Build a date range component for the last 90 days."
* "Create a custom date range from January 1 to March 31."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Project (`upsertProject`)

Creates a new workspace project or updates an existing one. If a `projectId` is provided, updates the existing project; if omitted, creates a new one. Before calling this tool, call `describeCja(PROJECT_BASE)` to learn the required project structure. For specific visualization types, also call `describeCja` with the appropriate guide type (for example, `PROJECT_VIZ_COMBO`, `PROJECT_VIZ_FLOW`, `PROJECT_FREEFORM_TABLE`). The `projectBody` must include `dataId` set to the data view ID; omitting `dataId` commonly causes "referenced component was not found in this data view" errors. The response automatically includes a `workspaceLink` field with a direct URL to open the project in Analysis Workspace.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `projectId` | No | String | The ID of the project to update. If not provided, creates a new project instead. |
| `projectBody` | Yes | Object | The project payload including `definition`, `dataId` (must be set to the data view ID), `type` (must be `project`), and optionally `name` and `description`. Call `describeCja(PROJECT_BASE)` for the full structure. |
| `expansions` | Yes | String | Additional data to return on the created or updated project. Available expansions:\<br/>• `dataId`: Includes the associated data view ID that the project is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the project. Useful for identifying the data source when working across multiple data views.\<br/>• `ownerFullName`: Includes the full name and login of the project owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the project was last modified.\<br/>• `definition`: Includes the full project definition as a JSON object, describing the panels, visualizations, freeform tables, and other components that make up the workspace project.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `approved`: Adds a boolean indicating whether the project has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the project, each containing the tag ID, name, and other metadata for organizational categorization.\<br/>• `folder`: Includes the folder location where the project is stored in the workspace. |

**Example prompts:**

* "Create a new workspace project with a freeform table showing page views by day."
* "Build a project with a bar chart of top pages by visits."
* "Update project proj12345 to add a new panel."
* "Create a workspace project with a flow visualization."
* "Build a marketing dashboard project."

<AccordionItem slots="heading, text, text, table, text, text"/>

### Create or Update Audience (`upsertAudience`)

Creates a new audience or updates an existing one. If an `audienceId` is provided, updates the existing audience; if omitted, creates a new one.

**Parameters:**

| Name | Required | Type | Description |
|------|----------|------|-------------|
| `audienceId` | No | String | The ID of the audience to update. If not provided, creates a new audience instead. |
| `audienceBody` | Yes | Object | The audience metadata and definition object. Includes fields such as `name`, `description`, and `definition`. |
| `expansions` | Yes | String | Additional data to return on the created or updated audience. Available expansions:\<br/>• `ownerFullName`: Includes the full name and login of the audience owner, expanding the `owner` object beyond just the user ID.\<br/>• `modified`: Adds an ISO 8601 timestamp showing when the audience was last modified.\<br/>• `definition`: Includes the full audience definition as a JSON object, describing the segment logic and criteria that determine audience membership.\<br/>• `componentType`: Adds a string field identifying the component type. Useful when working with mixed component lists.\<br/>• `compatibility`: Adds information about which products the audience is compatible with.\<br/>• `dataId`: Includes the associated data view ID that the audience is tied to.\<br/>• `dataName`: Includes the name of the data view associated with the audience. Useful for identifying the data source when working across multiple data views.\<br/>• `approved`: Adds a boolean indicating whether the audience has been approved or curated by an admin for organizational use.\<br/>• `tags`: Includes an array of tag objects associated with the audience, each containing the tag ID, name, and other metadata for organizational categorization. |

**Example prompts:**

* "Create an audience called 'High-value Customers'."
* "Update audience aud12345 with a new name."
* "Build an audience for users who completed a purchase."
