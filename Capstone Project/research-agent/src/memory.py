import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger("agent")

class VectorMemory:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.store = []  # keep raw text
    
    def add(self, text: str):
        logger.info("Memory: Adding new chunk")
        emb = self.model.encode([text])
        self.index.add(np.array(emb).astype("float32"))
        self.store.append(text)

    def search(self, query: str, k=3):
        logger.info("Memory: Searching")
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(np.array(q_emb).astype("float32"), k)

        results = [self.store[i] for i in indices[0] if i < len(self.store)]
        return results
