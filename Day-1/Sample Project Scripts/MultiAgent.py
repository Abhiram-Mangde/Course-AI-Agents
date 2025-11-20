from openai import OpenAI
client = OpenAI()

def llm(messages):
    return client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    ).choices[0].message.content

def researcher(topic):
    return llm([
        {"role": "system", "content": "You are a research agent. Give detailed findings."},
        {"role": "user", "content": topic}
    ])

def writer(info):
    return llm([
        {"role": "system", "content": "You are a writing agent. Create a concise summary."},
        {"role": "user", "content": info}
    ])

topic = "How tools extend AI agent capabilities"
raw_research = researcher(topic)
final_writeup = writer(raw_research)
print(final_writeup)
