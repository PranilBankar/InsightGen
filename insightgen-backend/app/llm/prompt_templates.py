"""Prompt templates for LLM interactions"""

SQL_GENERATION_PROMPT = """You are an expert SQL query generator for a PostgreSQL database.

DATABASE SCHEMA:
{schema_context}

USER QUESTION:
{user_question}

INSTRUCTIONS:
1. Generate a valid PostgreSQL SQL query that answers the user's question
2. Use ONLY the tables and columns defined in the schema above
3. Use proper JOINs when accessing data from multiple tables
4. Include appropriate WHERE clauses for filtering
5. Use GROUP BY for aggregations
6. Use ORDER BY to sort results logically
7. Add LIMIT clause if the query might return many rows (default: LIMIT 1000)
8. For date-based queries, use PostgreSQL date functions (DATE_TRUNC, EXTRACT, etc.)
9. Return ONLY the SQL query, no explanations or markdown formatting
10. Ensure the query is safe and read-only (SELECT only)

EXAMPLES:
Question: "Show monthly sales by category for last quarter"
SQL: SELECT p.category, DATE_TRUNC('month', o.order_date) as month, SUM(o.revenue) as total_revenue FROM orders o JOIN products p ON o.product_id = p.product_id WHERE o.order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY p.category, month ORDER BY month, p.category

Question: "Top 10 customers by revenue"
SQL: SELECT c.customer_name, c.region, SUM(o.revenue) as total_revenue FROM orders o JOIN customers c ON o.customer_id = c.customer_id GROUP BY c.customer_name, c.region ORDER BY total_revenue DESC LIMIT 10

Now generate the SQL query for the user's question above.

SQL Query:"""


VISUALIZATION_GENERATION_PROMPT = """You are a data visualization expert. Based on the SQL query and its results, determine the best chart type and configuration.

SQL QUERY:
{sql_query}

DATA PREVIEW (first 5 rows):
{data_preview}

COLUMN NAMES:
{column_names}

INSTRUCTIONS:
1. Analyze the data structure and determine the most appropriate chart type
2. Choose from: line, bar, pie, area, scatter
3. Identify which columns should be used for x-axis, y-axis, and grouping
4. Return a JSON object with the visualization configuration

CHART TYPE SELECTION GUIDE:
- **line**: Time series data, trends over time
- **bar**: Comparing categories, rankings
- **pie**: Showing proportions/percentages (max 10 categories)
- **area**: Cumulative trends over time
- **scatter**: Correlation between two numeric variables

Return ONLY a valid JSON object in this exact format (no markdown, no explanations):
{{
  "chart_type": "line|bar|pie|area|scatter",
  "title": "Descriptive chart title",
  "x_axis": "column_name_for_x_axis",
  "y_axis": "column_name_for_y_axis",
  "group_by": "column_name_for_grouping (optional, can be null)",
  "aggregation": "sum|avg|count|none"
}}

Visualization Config:"""


INSIGHT_GENERATION_PROMPT = """You are a business analyst. Analyze the following data and generate actionable insights.

USER QUESTION:
{user_question}

SQL QUERY EXECUTED:
{sql_query}

DATA SUMMARY:
{data_summary}

INSTRUCTIONS:
1. Identify key trends, patterns, or anomalies in the data
2. Highlight significant growth or decline
3. Compare performance across categories/regions if applicable
4. Provide 2-4 concise, actionable insights
5. Use specific numbers and percentages
6. Write in clear, business-friendly language

Return ONLY a JSON array of insight strings (no markdown, no explanations):
["Insight 1", "Insight 2", "Insight 3"]

Insights:"""
