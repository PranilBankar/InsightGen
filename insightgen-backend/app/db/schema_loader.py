"""Schema metadata loader for LLM context"""
import json
from typing import Dict, Any


# Database schema metadata for LLM
SCHEMA_METADATA = {
    "database": "insightgen",
    "description": "Sales and e-commerce database containing product catalog, customer information, and order transactions",
    "tables": {
        "products": {
            "description": "Product catalog with pricing and category information",
            "columns": {
                "product_id": {
                    "type": "INTEGER",
                    "description": "Unique product identifier (primary key)"
                },
                "product_name": {
                    "type": "VARCHAR(255)",
                    "description": "Name of the product"
                },
                "category": {
                    "type": "VARCHAR(100)",
                    "description": "Product category (e.g., Electronics, Clothing, Home & Garden, Sports, Books)"
                },
                "price": {
                    "type": "NUMERIC(10,2)",
                    "description": "Product unit price in dollars"
                }
            },
            "sample_values": {
                "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
            }
        },
        "customers": {
            "description": "Customer information including name and geographic region",
            "columns": {
                "customer_id": {
                    "type": "INTEGER",
                    "description": "Unique customer identifier (primary key)"
                },
                "customer_name": {
                    "type": "VARCHAR(255)",
                    "description": "Customer full name"
                },
                "region": {
                    "type": "VARCHAR(100)",
                    "description": "Geographic region where customer is located"
                }
            },
            "sample_values": {
                "region": ["North", "South", "East", "West"]
            }
        },
        "orders": {
            "description": "Sales order transactions linking customers and products with revenue data",
            "columns": {
                "order_id": {
                    "type": "INTEGER",
                    "description": "Unique order identifier (primary key)"
                },
                "customer_id": {
                    "type": "INTEGER",
                    "description": "Foreign key reference to customers table"
                },
                "product_id": {
                    "type": "INTEGER",
                    "description": "Foreign key reference to products table"
                },
                "order_date": {
                    "type": "DATE",
                    "description": "Date when the order was placed (format: YYYY-MM-DD)"
                },
                "quantity": {
                    "type": "INTEGER",
                    "description": "Number of items ordered"
                },
                "revenue": {
                    "type": "NUMERIC(10,2)",
                    "description": "Total revenue from this order in dollars (quantity * price)"
                }
            },
            "relationships": {
                "customer": "JOIN customers ON orders.customer_id = customers.customer_id",
                "product": "JOIN products ON orders.product_id = products.product_id"
            }
        }
    },
    "common_queries": [
        {
            "question": "Show sales trends by category",
            "sql": "SELECT p.category, DATE_TRUNC('month', o.order_date) as month, SUM(o.revenue) as total_revenue FROM orders o JOIN products p ON o.product_id = p.product_id GROUP BY p.category, month ORDER BY month"
        },
        {
            "question": "Top selling products",
            "sql": "SELECT p.product_name, SUM(o.quantity) as total_quantity, SUM(o.revenue) as total_revenue FROM orders o JOIN products p ON o.product_id = p.product_id GROUP BY p.product_name ORDER BY total_revenue DESC LIMIT 10"
        }
    ]
}


def get_schema_context() -> str:
    """
    Get formatted schema context for LLM prompts
    Returns a string representation of the database schema
    """
    return json.dumps(SCHEMA_METADATA, indent=2)


def get_table_info(table_name: str) -> Dict[str, Any]:
    """Get information about a specific table"""
    return SCHEMA_METADATA["tables"].get(table_name, {})


def get_all_tables() -> list:
    """Get list of all available tables"""
    return list(SCHEMA_METADATA["tables"].keys())
