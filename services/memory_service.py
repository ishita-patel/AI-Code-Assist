import chromadb
from chromadb.config import Settings

class MemoryClient:
    def __init__(self):
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"  # Directory to store ChromaDB data
        ))
        # Create or load a collection for code interactions
        self.collection = self.client.get_or_create_collection(name="code_interactions")

    def add_memory(self, session_id: str, prompt: str, response: str):
        # Store a new interaction in the collection
        self.collection.add(
            documents=[response],  # The generated code/reasoning
            metadatas={"session_id": session_id, "prompt": prompt},  # Metadata for context
            ids=[session_id]  # Unique ID for the interaction
        )

    def get_memory(self, session_id: str):
        # Retrieve past interactions for a given session
        return self.collection.get(ids=[session_id])
    