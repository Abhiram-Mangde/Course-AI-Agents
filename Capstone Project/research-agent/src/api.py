from fastapi import FastAPI
from agent import ResearchAgent
from logging_config import setup_logging

logger = setup_logging()

app = FastAPI()
agent = ResearchAgent()

@app.get("/research")
def research_endpoint(topic: str):
    logger.info(f"API Request: topic={topic}")
    result = agent.research(topic)
    return {"report": result}
