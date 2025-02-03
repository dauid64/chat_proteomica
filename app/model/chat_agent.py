from qdrant_client import QdrantClient

class ChatAgent:
    def __init__(self, conn: QdrantClient):
        self.conn = conn
    
    