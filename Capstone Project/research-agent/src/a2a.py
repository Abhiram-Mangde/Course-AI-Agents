import logging
logger = logging.getLogger("agent")

def planner_agent(topic: str):
    logger.info("A2A: Planner Agent invoked")
    return {
        "steps": [
            "Search topic online",
            "Store findings in memory",
            "Retrieve memory",
            "Summarize findings",
            "Generate final report"
        ]
    }

def executor_agent(steps):
    logger.info("A2A: Executor received plan")
    return f"Executor acknowledges {len(steps)} steps."
