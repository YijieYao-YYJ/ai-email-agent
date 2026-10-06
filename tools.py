import sqlite3
from pathlib import Path


# orders.db 永远定位到 tools.py 所在的项目目录
DB_PATH = Path(__file__).resolve().parent / "orders.db"


def get_order_status(order_id):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT status, carrier, estimated_delivery
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        )

        row = cursor.fetchone()

    if row is None:
        return {
            "found": False,
            "error": "Order not found"
        }

    return {
        "found": True,
        "status": row[0],
        "carrier": row[1],
        "estimated_delivery": row[2]
    }


def get_customer(customer_id):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT customer_id, name, email
            FROM customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        row = cursor.fetchone()

    if row is None:
        return {
            "found": False,
            "error": "Customer not found"
        }

    return {
        "found": True,
        "customer_id": row[0],
        "name": row[1],
        "email": row[2]
    }


def get_customer_by_email(email):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT customer_id, name, email
            FROM customers
            WHERE email = ?
            """,
            (email,)
        )

        row = cursor.fetchone()

    if row is None:
        return {
            "found": False,
            "error": "Customer not found"
        }

    return {
        "found": True,
        "customer_id": row[0],
        "name": row[1],
        "email": row[2]
    }


def get_orders_by_customer(customer_id):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT order_id, status, carrier, estimated_delivery
            FROM orders
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        rows = cursor.fetchall()

    if not rows:
        return {
            "found": False,
            "orders": []
        }

    return {
        "found": True,
        "orders": [
            {
                "order_id": row[0],
                "status": row[1],
                "carrier": row[2],
                "estimated_delivery": row[3]
            }
            for row in rows
        ]
    }