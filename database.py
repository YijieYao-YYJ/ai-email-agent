import sqlite3


connection = sqlite3.connect("orders.db")
cursor = connection.cursor()


# =========================
# Customers
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")


cursor.execute("""
INSERT OR IGNORE INTO customers
(customer_id, name, email)
VALUES (?, ?, ?)
""", ("C001", "Max Mustermann", "max@example.com"))


cursor.execute("""
INSERT OR IGNORE INTO customers
(customer_id, name, email)
VALUES (?, ?, ?)
""", ("C002", "Anna Schmidt", "anna@example.com"))


# =========================
# Orders
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    carrier TEXT,
    estimated_delivery TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")


cursor.execute("""
INSERT OR IGNORE INTO orders
(order_id, customer_id, status, carrier, estimated_delivery)
VALUES (?, ?, ?, ?, ?)
""", ("12345", "C001", "shipped", "DHL", "tomorrow"))


cursor.execute("""
INSERT OR IGNORE INTO orders
(order_id, customer_id, status, carrier, estimated_delivery)
VALUES (?, ?, ?, ?, ?)
""", ("67890", "C002", "processing", None, None))


cursor.execute("""
INSERT OR IGNORE INTO orders
(order_id, customer_id, status, carrier, estimated_delivery)
VALUES (?, ?, ?, ?, ?)
""", ("54321", "C001", "processing", None, None))


connection.commit()
connection.close()

print("Database created successfully!")