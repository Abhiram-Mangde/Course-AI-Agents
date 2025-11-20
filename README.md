# Course-AI-Agents
This short course introduces the full lifecycle of modern AI Agents

## Brief Architecture Summary

The **Research & Report AI** Agent follows a modular, production-ready architecture:

### 1. API Layer (FastAPI)
- Receives topic requests and routes them to the agent.

### 2. Research Agent (Core Logic)
- Accepts the user topic
- Calls external Tools (e.g., web search)
- Stores findings into Vector Memory (FAISS + embeddings)
- Retrieves top-K relevant chunks
- Summarizes data into a structured Final Report

### 3. Tools Layer
- web_search() retrieves information (mock or real API)
- Future tools can be added: crawlers, databases, APIs

### 4. Vector Memory (FAISS)
- Stores research chunks
- Enables semantic search
- Supports retrieval-augmented generation (RAG)

### 5. Observability / Logging
- Logs tool calls, memory usage, API requests, execution steps, errors, and latency.

### 6. Optional A2A Multi-Agent Layer
- Planner Agent → creates the research plan
- Executor Agent → performs the steps
- Allows chain-of-agents workflows

### 7. Deployment Layer (Docker)
- Reproducible container
- Runs API + agent stack in production