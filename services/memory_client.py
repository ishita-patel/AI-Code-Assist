import chromadb
from chromadb.config import Settings
from typing import Dict, Optional, List

class MemoryClient:
    def __init__(self):
        """
        Initialize the ChromaDB client with persistent storage.
        """
        # Configure ChromaDB settings
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",  # Use DuckDB with Parquet for storage
            persist_directory="./chroma_db"    # Directory to store the database
        ))
        # Create or load a collection for code interactions
        self.collection = self.client.get_or_create_collection(name="code_interactions")

    def add_memory(self, session_id: str, prompt: str, response: str) -> None:
        """
        Store a new interaction in the database.

        Args:
            session_id (str): Unique ID for the session.
            prompt (str): The user's prompt.
            response (str): The generated code/reasoning.
        """
        try:
            self.collection.add(
                documents=[response],  # The generated code/reasoning
                metadatas={"session_id": session_id, "prompt": prompt},  # Metadata for context
                ids=[session_id]  # Unique ID for the interaction
            )
        except Exception as e:
            print(f"Error adding memory to ChromaDB: {e}")
            raise

    def get_memory(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve past interactions for a given session.

        Args:
            session_id (str): Unique ID for the session.

        Returns:
            Optional[Dict]: The stored interaction or None if not found.
        """
        try:
            result = self.collection.get(ids=[session_id])
            return result
        except Exception as e:
            print(f"Error retrieving memory from ChromaDB: {e}")
            return None