"""
This file contains the RAG pipeline.
"""

import os
import uuid

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")


class QdrantVectorStore:
    """
    Qdrant vector store implementation for managing vector embeddings
    Handles connection, data insertion, and search operations with a Qdrant database
    """

    def __init__(self, tenant_id, *args, **kwargs):
        """
        Initialize the vector store

        Args:
            tenant_id: Identifier for the organization/tenant
            *args, **kwargs: Additional arguments passed to parent class
        """
        super().__init__(*args, **kwargs)
        self.tenant_id = tenant_id
        self.client = self.connect()

    def connect(self):
        """
        Establish connection to the Qdrant vector store

        Returns:
            QdrantClient: Connected client instance

        Raises:
            Exception: If connection fails
        """
        if self.client is None:
            try:
                qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
                self.client = qdrant_client
            except Exception as e:
                raise e

        return self.client

    def insert_data_to_qdrant(self, collection_name: str, vector_payload: list):
        """
        Insert vector embeddings and their associated payloads into Qdrant

        Args:
            collection_name (str): Name of the collection to insert data into
            vector_payload (list): List of dictionaries containing vectors and payloads
                                   Each dict should have 'vector' and 'payload' keys

        Returns:
            info: Response from Qdrant about the insertion operation
        """
        info = self.client.upsert(
            collection_name=collection_name,
            wait=True,  # Wait for operation to complete
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),  # Generate unique ID for each point
                    vector=vector_set.get("vector"),  # The vector embedding
                    payload=vector_set.get("payload"),  # Associated metadata/payload
                )
                for vector_set in vector_payload
            ],
        )

        return info

    def search_data_from_qdrant(
        self, collection_name: str, query: str, tenant_id: str = None, limit: int = 5
    ):
        """
        Search data from Qdrant vector database

        Args:
            collection_name (str): Name of the Qdrant collection to search in
            query (str): The search query text
            tenant_id (str): Optional filter to search for specific tenant_id
            limit (int): Maximum number of results to return (default: 10)

        Returns:
            List of search results from Qdrant, ordered by relevance
        """
        # Initialize empty filter list for search conditions
        filter_list = []

        # If tenant_id is provided, add it as a filter condition
        if tenant_id:
            filter_list.append(
                models.FieldCondition(
                    key="tenant_id", match=models.MatchValue(value=tenant_id)
                )
            )

        # Perform the search using Qdrant client
        return self.client.search(
            collection_name=collection_name,
            query_text=query,
            tenant_id=tenant_id,
            limit=limit,
        )
