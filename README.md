# AI Email Agent

An AI-powered customer service agent built with Python, Anthropic Claude, Tool Calling, and SQLite.

The agent can understand customer emails, decide which tools are required, retrieve customer and order information from a database, perform multi-step tool calls, and generate context-aware customer responses.

---

## Features

- AI-powered customer email understanding
- Anthropic Claude Tool Calling
- Multi-step Agent Loop
- Dynamic tool selection
- Sequential tool execution
- Customer lookup by email
- Customer lookup by customer ID
- Order lookup by order ID
- Order lookup by customer ID
- Multiple-order handling
- SQLite database integration
- Missing-information handling
- Tool and API error handling
- Maximum iteration protection
- Hallucination-reduction rules
- Application logging
- Modular Python architecture

---

## How It Works

Example customer email:

```text
Hallo,

meine E-Mail-Adresse ist max@example.com.
Wo ist meine Bestellung?

Viele Grüße
```

The agent can perform the following workflow:

```text
Customer Email
      |
      v
Claude AI Agent
      |
      | decides which tool is needed
      v
get_customer_by_email
      |
      | customer_id = C001
      v
Claude AI Agent
      |
      | uses information from previous tool result
      v
get_orders_by_customer
      |
      v
SQLite Database
      |
      | returns order data
      v
Claude AI Agent
      |
      v
Customer Response
```

The model does not directly access the database.

Claude decides which tools are required, while Python executes the actual operations and returns the results to the model.

---

# Demo

## Demo 1 — Sequential Tool Calling

A customer asks about an order but provides only an email address:

```text
Hallo,

meine E-Mail-Adresse ist max@example.com.
Wo ist meine Bestellung?

Viele Grüße
```

The agent first identifies the customer:

```text
Tool: get_customer_by_email
Input: {'email': 'max@example.com'}

Tool Result:
{
    'found': True,
    'customer_id': 'C001',
    'name': 'Max Mustermann',
    'email': 'max@example.com'
}
```

The agent then uses the `customer_id` returned by the first tool to perform a second tool call:

```text
Tool: get_orders_by_customer
Input: {'customer_id': 'C001'}

Tool Result:
{
    'found': True,
    'orders': [
        {
            'order_id': '12345',
            'status': 'shipped',
            'carrier': 'DHL',
            'estimated_delivery': 'tomorrow'
        },
        {
            'order_id': '54321',
            'status': 'processing',
            'carrier': None,
            'estimated_delivery': None
        }
    ]
}
```

The retrieved information is then used to generate the customer-facing response:

```text
Guten Tag, Herr Mustermann,

ich konnte zwei Bestellungen in Ihrem Konto finden:

| Bestellnummer | Status | Versanddienstleister | Voraussichtliche Lieferung |
|---------------|--------|----------------------|----------------------------|
| 12345 | Versandt | DHL | Morgen |
| 54321 | In Bearbeitung | – | – |

Meinen Sie eine bestimmte Bestellung, oder möchten Sie zu beiden Informationen?

Viele Grüße
```

The workflow is:

```text
Customer Email
      ↓
Claude
      ↓
get_customer_by_email
      ↓
customer_id = C001
      ↓
Claude
      ↓
get_orders_by_customer
      ↓
Order Data
      ↓
Claude
      ↓
Final Response
```

The second tool call depends on information obtained from the first tool call rather than following a hard-coded sequence.

---

## Demo 2 — Missing Information Handling

If the customer does not provide enough information:

```text
Wo ist meine Bestellung?
```

The agent does not guess an order number or call a tool with fabricated information.

Instead, it asks the customer for the information required to perform a reliable lookup:

```text
Gerne helfe ich Ihnen dabei.

Bitte teilen Sie mir Ihre Bestellnummer oder die E-Mail-Adresse mit,
die Sie für die Bestellung verwendet haben.
```

No tool is executed because the required lookup information is missing.

```text
Customer Email
      ↓
Claude
      ↓
Required information available?
      ↓
     No
      ↓
Ask Customer for Missing Information
```

This prevents the agent from inventing identifiers or performing unreliable database queries.

---

## Demo 3 — Order Not Found

If the customer provides an order number that does not exist:

```text
Hallo,

wo ist meine Bestellung 99999?

Viele Grüße
```

The agent calls the appropriate lookup tool:

```text
Tool: get_order_status
Input: {'order_id': '99999'}

Tool Result:
{
    'found': False,
    'error': 'Order not found'
}
```

The agent does not invent an order status, carrier, tracking number, or delivery date.

Instead, it explains that the requested order could not be found:

```text
Leider konnte ich unter der Bestellnummer 99999 keine Bestellung finden.

Bitte überprüfen Sie die Bestellnummer oder teilen Sie mir die
E-Mail-Adresse mit, die Sie für die Bestellung verwendet haben.

Viele Grüße
```

The workflow is:

```text
Customer provides order 99999
          ↓
Claude
          ↓
get_order_status
          ↓
found = false
          ↓
Claude
          ↓
Explain that the order could not be found
          ↓
Do not invent order information
```

This demonstrates how the agent handles unsuccessful database lookups without fabricating business data.

---

## Demo 4 — Tool Error Handling

The agent also handles unexpected failures inside Python tools.

For example, if a database query fails:

```text
Claude
   ↓
Tool Call
   ↓
Python Tool
   ↓
Database Error
```

The exception is caught by the application.

Detailed technical information is written to the internal application log:

```text
ERROR | Tool failed: get_customer_by_email

Traceback (most recent call last):
...
sqlite3.OperationalError: ...
```

However, the detailed internal exception is not returned to Claude.

The tool result exposed to the agent is reduced to:

```text
{
    "error": "Tool execution failed"
}
```

Claude can then provide a safe customer-facing response without exposing database internals:

```text
Leider ist ein technisches Problem aufgetreten.

Bitte versuchen Sie es später erneut.

Viele Grüße
```

The error flow is:

```text
Customer Request
      ↓
Claude
      ↓
Tool Call
      ↓
Python Tool
      ↓
Exception
   ↙       ↘
Internal   Safe Tool Result
Logging          ↓
                 Claude
                   ↓
          Customer-safe Response
```

This separates developer diagnostics from customer-facing information.

---

## Available Tools

### `get_order_status`

Retrieves the current status and shipping information for a specific order.

### `get_customer`

Retrieves customer information using a customer ID.

### `get_customer_by_email`

Finds a customer using their email address.

### `get_orders_by_customer`

Retrieves all orders associated with a customer.

---

## Agent Architecture

The project separates AI reasoning, tool definitions, business logic, data storage, and logging.

```text
                    Customer Email
                          |
                          v
                       main.py
                          |
                          v
                       agent.py
                          |
                 +--------+--------+
                 |                 |
                 v                 v
             Claude API       tool_config.py
                                   |
                                   v
                               Tool Registry
                                   |
                                   v
                                tools.py
                                   |
                                   v
                                SQLite

                       agent.py
                          |
                          v
                       logger.py
                          |
                          v
                    logs/agent.log
```

Claude is responsible for reasoning and tool selection.

Python is responsible for executing tools and controlling the Agent Loop.

SQLite stores the example customer and order data.

---

## Project Structure

```text
ai-email-agent/
│
├── main.py
├── agent.py
├── tool_config.py
├── tools.py
├── database.py
├── logger.py
├── orders.db
├── logs/
├── .env
├── .gitignore
└── README.md
```

### `main.py`

Entry point for the application and example customer email.

### `agent.py`

Contains the Claude client, system prompt, Agent Loop, Tool Calling logic, and error handling.

### `tool_config.py`

Defines the tool schemas available to Claude and maps tool names to Python functions.

### `tools.py`

Contains the Python functions that query the SQLite database.

### `database.py`

Creates and initializes the example customer and order database.

### `logger.py`

Configures application logging.

---

## Reliability and Safety

The agent includes several safeguards:

- Tool execution exceptions are caught and handled.
- Anthropic API errors are caught and logged.
- Detailed internal errors are separated from customer-facing responses.
- Tool results distinguish successful and unsuccessful lookups.
- Missing information causes the agent to ask for clarification instead of guessing.
- Missing database values are treated as unknown.
- Status values are treated literally instead of being used to infer unsupported business facts.
- A maximum Agent Loop iteration count prevents infinite execution.
- System prompt rules reduce unsupported business-information generation.
- API credentials are stored outside the source code.

---

## Agent Loop

The agent can perform multiple reasoning and tool execution cycles.

```text
Send Messages to Claude
          ↓
Claude Response
          ↓
Tool Call?
     ↙          ↘
   Yes           No
    ↓             ↓
Execute Tool   Final Answer
    ↓
Tool Result
    ↓
Add Result to Conversation
    ↓
Send Back to Claude
    ↓
Repeat
```

The loop is protected by a maximum iteration limit.

---

## Logging

The application uses Python's `logging` module to record agent activity and errors.

Example:

```text
INFO | Tool requested: get_customer_by_email
INFO | Tool completed: get_customer_by_email
INFO | Tool requested: get_orders_by_customer
INFO | Tool completed: get_orders_by_customer
```

Unexpected exceptions are logged with traceback information:

```text
ERROR | Tool failed: get_customer_by_email
Traceback (most recent call last):
...
```

Detailed exceptions remain available for debugging without being exposed in customer-facing responses.

---

## Technologies

- Python 3.13
- Anthropic Claude API
- Claude Tool Calling
- SQLite
- python-dotenv
- Python logging
- Git
- GitHub

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YijieYao-YYJ/ai-email-agent.git
cd ai-email-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install anthropic python-dotenv
```

### 4. Configure the API key

Create a `.env` file in the project directory:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git.

### 5. Initialize the database

```bash
python database.py
```

This creates the example SQLite database and sample customer/order data.

### 6. Run the agent

```bash
python main.py
```

---

## Example Data

The demo database contains example customers and orders such as:

```text
Customer:
C001
Max Mustermann
max@example.com

Orders:
12345 — shipped — DHL — tomorrow
54321 — processing
```

The data is fictional and used only to demonstrate the Agent workflow.

---

## Security

API credentials are stored using environment variables and are excluded from Git using `.gitignore`.

Runtime files are also excluded from the repository:

```text
.env
.venv/
logs/
*.db
.idea/
__pycache__/
```

Detailed internal tool errors are logged locally instead of being sent to the AI model or exposed to customers.

---

## Current Status

This repository demonstrates the core architecture of an AI customer service agent.

The current version supports:

```text
Customer Message
      ↓
AI Reasoning
      ↓
Dynamic Tool Selection
      ↓
Python Tool Execution
      ↓
SQLite Data Retrieval
      ↓
Multi-step Agent Loop
      ↓
Customer Response
```

The current implementation uses a local SQLite database and example customer/order data.

It is intended as a portfolio and technical demonstration rather than a production customer-support system.

---

## Possible Future Extensions

Possible extensions include:

- Gmail integration
- Microsoft Outlook integration
- Human approval before sending AI-generated responses
- Shopify integration
- WooCommerce integration
- Integration with real CRM or ERP systems
- Web-based operator interface
- Authentication and permissions
- Deployment as a hosted service
- Monitoring and analytics
- Multi-tenant customer configuration

---

## License

This project is currently intended as a portfolio and educational project.