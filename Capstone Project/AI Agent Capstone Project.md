# Research & Report AI Agent 

*Tools • Memory • Observability • MCP • Optional A2A Agents*
---

## Overview

This project implements a production-ready **Research & Report AI Agent:**
- Accepts a **topic** from the user
- Uses a search tool to gather information
- Stores findings in **vector memory**
- Summarizes the research
- Generates a final structured report
- Includes:
    - Tool Integration
    - Vector Memory
    - Observability Logging
    - A2A Multi-Agent Option
    - API Ready Deployment

## Folder Structure:

```
research-agent/
│
├── src/
│   ├── agent.py
│   ├── tools.py
│   ├── memory.py
│   ├── logging_config.py
│   ├── a2a.py
│   ├── api.py
│   └── config.py
│
├── README.md
├── requirements.txt
└── Dockerfile

```
---
## Concepts Used in This Project

**1.Tools** 

Agents require tools to interact with the outside world.
Here, we create:
- `web_search(query)` — simulated or real API
- You can replace with Google/Bing/Tavily API

**2. Vector Memory**

We store research chunks in a **FAISS vector DB**, allowing:
- Semantic search
- Retrieval-augmented generation
- Persistent storage

**3. Observability**

*We log:*
- Tool calls
- Inputs/Outputs
- Reasoning steps
- Errors
- Latency

*Logging is essential for debugging multi-step agents.*

---

## A2A (Agent-to-Agent Protocol) (optional)

**Two agents:**

- Planner Agent → determines research plan
- Research Agent → executes the plan

---

## How It Works (Step-by-Step)
- User sends a topic
    - /research?topic=climate change

- Agent calls search tool
    - web_search("climate change")

- Results go into vector memory
    - FAISS index stores embeddings.

- Agent retrieves relevant context
    - Semantic search refines information.

- Agent summarizes info
    - (RAG-style summarization)

- Returns final report
---

## Running the Project

**Clone**
```bash
git clone https://github.com/yourname/research-agent
cd research-agent
```

**Install**
```bash
pip install -r requirements.txt
```

**Run API**
```bash
uvicorn api:app --reload
```

**Request**
```
http://localhost:8000/research?topic=ai%20agents
```
---