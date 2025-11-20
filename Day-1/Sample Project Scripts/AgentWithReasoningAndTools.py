import re
from openai import OpenAI
client = OpenAI()

def add_tool(a: int, b: int):
    """Simple tool to add two numbers."""
    return {"result": a + b}

def agent_v2(message):
    # Ask LLM if a tool is needed
    system_prompt = """
    You are a math assistant agent.
    If user asks to add numbers, respond with:
    TOOL: {"a": x, "b": y}
    Otherwise answer directly.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    content = response.choices[0].message.content

    # Check if LLM decided to use the tool
    if content.startswith("TOOL:"):
        data = eval(content.replace("TOOL:", "").strip())
        tool_output = add_tool(data["a"], data["b"])
        return f"Tool result: {tool_output['result']}"
    else:
        return content


print(agent_v2("Can you add 12 and 8?"))
