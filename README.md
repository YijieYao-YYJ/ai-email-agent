# AI Email Agent

An AI-powered customer service agent built with Python, Anthropic Claude, Tool Calling, and SQLite.

The agent can understand customer emails, decide which tools are required, retrieve customer and order information from a database, and generate context-aware responses.

## Features

- AI-powered customer email understanding
- Anthropic Claude Tool Calling
- Multi-step Agent Loop
- Dynamic tool selection
- Sequential tool execution
- Customer lookup by email
- Order lookup by customer ID
- Multiple-order handling
- SQLite database integration
- Missing-information handling
- Tool and API error handling
- Maximum iteration protection
- Hallucination-reduction rules
- Application logging
- Modular Python architecture

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

The model does not directly access the database. It selects tools through Tool Calling, while Python executes the actual operations.

## Example

Tool calls:

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

The agent can then use the returned customer ID for another tool call:

```text
Tool: get_orders_by_customer
Input: {'customer_id': 'C001'}
```

Example final response:

```text
Hallo Max Mustermann,

ich habe zwei Bestellungen in Ihrem Konto gefunden:

12345 - Versandt - DHL - Morgen
54321 - In Bearbeitung

Könnten Sie mir bitte mitteilen, nach welcher Bestellung Sie fragen?
```

## Available Tools

### `get_order_status`

Retrieves the current status and shipping information for a specific order.

### `get_customer`

Retrieves customer information using a customer ID.

### `get_customer_by_email`

Finds a customer using their email address.

### `get_orders_by_customer`

Retrieves all orders associated with a customer.

## Agent Architecture

The project separates AI reasoning, tool definitions, business logic, and data storage.

```text
main.py
   |
   v
agent.py
   |
   +---- Claude API
   |
   +---- tool_config.py
              |
              v
           tools.py
              |
              v
           SQLite
```

### File Structure

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

## Reliability and Safety

The agent includes several safeguards:

- Tool execution errors are caught and handled.
- API errors are logged without exposing internal details to customers.
- Tool results distinguish successful and unsuccessful lookups.
- A maximum Agent Loop iteration count prevents infinite execution.
- Missing database values are treated as unknown instead of guessed.
- The system prompt prevents unsupported business information from being invented.
- Detailed internal errors are separated from customer-facing error messages.

## Logging

The application records agent activity and errors using Python's `logging` module.

Example:

```text
INFO | Tool requested: get_customer_by_email
INFO | Tool completed: get_customer_by_email
INFO | Tool requested: get_orders_by_customer
INFO | Tool completed: get_orders_by_customer
```

Detailed exceptions are stored internally while customer-facing responses remain concise.

## Technologies

- Python 3.13
- Anthropic Claude API
- Tool Calling
- SQLite
- python-dotenv
- Python logging

## Setup

Install the required dependencies:

```bash
pip install anthropic python-dotenv
```

Create a `.env` file:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Initialize the example database:

```bash
python database.py
```

Run the agent:

```bash
python main.py
```

## Security

API keys are stored in environment variables and are excluded from Git using `.gitignore`.

The project does not hard-code API credentials in the source code.

## Current Status

This version demonstrates the core architecture of an AI customer service agent.

The current implementation uses a local SQLite database and example customer/order data.

Possible future extensions include:

- Gmail or Microsoft Outlook integration
- Human approval before sending responses
- Integration with real e-commerce systems
- Web interface
- Authentication and permissions
- Deployment as a hosted service

## License

This project is intended as a portfolio and educational project.