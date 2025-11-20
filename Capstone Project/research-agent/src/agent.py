import logging
from tools import web_search
from memory import VectorMemory

logger = logging.getLogger("agent")

class ResearchAgent:
    def __init__(self):
        self.memory = VectorMemory()

    def research(self, topic: str):
        logger.info(f"Agent Research Start: {topic}")

        # 1. Search
        results = web_search(topic)

        # 2. Store in memory
        for r in results:
            chunk = r["content"]
            self.memory.add(chunk)

        # 3. Retrieve relevant info
        retrieved = self.memory.search(topic)

        # 4. Summarize (simple version)
        summary = "\n".join(retrieved)

        # 5. Final report
        report = f"""
        # Research Report: {topic}

        ## Key Findings
        {summary}

        ## Source Count
        {len(results)} results stored
        """
        return report
