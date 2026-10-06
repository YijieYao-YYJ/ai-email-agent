from tools import (
    get_order_status,
    get_customer,
    get_customer_by_email,
    get_orders_by_customer
)


# =========================
# Tool definitions for Claude
# =========================

tools = [
    {
        "name": "get_order_status",
        "description": "Get the current status and shipping information for an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order number, for example 12345."
                }
            },
            "required": ["order_id"]
        }
    },

    {
        "name": "get_customer",
        "description": "Get customer information using a customer ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID, for example C001."
                }
            },
            "required": ["customer_id"]
        }
    },

    {
        "name": "get_customer_by_email",
        "description": "Find a customer using their email address.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The customer's email address."
                }
            },
            "required": ["email"]
        }
    },

    {
        "name": "get_orders_by_customer",
        "description": "Get all orders belonging to a customer using their customer ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID, for example C001."
                }
            },
            "required": ["customer_id"]
        }
    }
]


# =========================
# Tool Registry
# =========================

tool_functions = {
    "get_order_status": get_order_status,
    "get_customer": get_customer,
    "get_customer_by_email": get_customer_by_email,
    "get_orders_by_customer": get_orders_by_customer
}