import os
import json

from dotenv import load_dotenv
from anthropic import Anthropic

from tool_config import tools, tool_functions
from logger import logger


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY was not found.")

client = Anthropic(api_key=api_key)


system_prompt = """
You are a customer service AI agent.

Rules:
- Use only information provided by the customer and information returned by tools.

- Never invent or assume order information, customer information, tracking numbers,
  delivery details, company policies, refund policies, contact information,
  customer names, or other business information.

- Do not infer business facts that are not explicitly provided by the customer
  or returned by a tool.

- Treat status values literally. Do not infer additional facts from a status.
  For example, "processing" does not mean "not shipped" unless a tool explicitly
  provides shipping information confirming that.

- If a value returned by a tool is null, None, missing, or unavailable,
  treat that information as unknown. Do not guess or infer the missing value.

- If the customer's name is unknown, do not invent or assume a name.

- If information required by a tool is missing, ask the customer for that information.

- If a tool returns found=false, clearly explain that the requested information
  could not be found. Do not invent possible reasons unless that information
  is available from a tool.

- If a tool returns an error, do not expose internal technical details to the customer.
  Explain only that a technical problem occurred.

- If multiple orders are found and the customer's request is ambiguous,
  present the available orders or ask which order they mean.

- Use tools when they are necessary to answer the customer's question.

- Do not claim that you performed an action unless a tool actually performed that action.

- Reply in the same language as the customer.

- Keep the response professional and concise.
"""


def run_agent(email):

    messages = [
        {
            "role": "user",
            "content": email
        }
    ]

    max_iterations = 10

    for iteration in range(max_iterations):

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                system=system_prompt,
                tools=tools,
                messages=messages
            )

        except Exception as e:
            print("\n--- API Error ---")
            print(e)
            logger.exception("Anthropic API request failed")

            return (
                "Entschuldigung, der AI-Service ist derzeit nicht verfügbar. "
                "Bitte versuchen Sie es später erneut."
            )

        messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

        tool_calls = []

        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append(block)

        # 如果 Claude 不需要继续调用工具，
        # 收集所有 text block 并作为最终答案返回
        if not tool_calls:
            text_blocks = [
                block.text
                for block in response.content
                if block.type == "text"
            ]

            return "\n".join(text_blocks)

        tool_results = []

        for block in tool_calls:
            tool_name = block.name
            tool_input = block.input

            print("\n--- Claude wants to use tool ---")
            print("Tool:", tool_name)
            print("Input:", tool_input)

            logger.info(
                "Tool requested: %s | Input: %s",
                tool_name,
                tool_input
            )

            if tool_name not in tool_functions:
                result = {
                    "error": f"Unknown tool: {tool_name}"
                }
            else:
                function = tool_functions[tool_name]

                try:
                    result = function(**tool_input)

                except Exception as e:
                    logger.exception(
                        "Tool failed: %s",
                        tool_name
                    )

                    result = {
                        "error": "Tool execution failed"
                    }

            print("--- Tool Result ---")
            print(result)

            logger.info(
                "Tool completed: %s | Result: %s",
                tool_name,
                result
            )

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False)
                }
            )

        messages.append(
            {
                "role": "user",
                "content": tool_results
            }
        )

    return "The agent reached the maximum number of iterations."