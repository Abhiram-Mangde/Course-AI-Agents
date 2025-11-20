from openai import OpenAI
client = OpenAI()

def search_weather(city):
    return {"temp": 20, "condition": "Cloudy"}

tools = [
  {
    "type": "function",
    "function": {
      "name": "search_weather",
      "description": "Get weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        },
        "required": ["city"]
      }
    }
  }
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "What's the weather like in Paris?"}],
    tools=tools
)

tool_call = response.choices[0].message.tool_calls[0]
city = tool_call['function']['arguments']['city']

result = search_weather(city)

print(result)
