import os

from vector_server.datastore.datastore import DataStore
from vector_server.datastore.providers.pinecone_datastore import PineconeDataStore


async def get_datastore() -> DataStore:
    datastore = os.environ.get("DATASTORE")
    assert datastore is not None

    match datastore:
        case "pinecone":

            return PineconeDataStore()

        case _:
            raise ValueError(
                f"Unsupported vector database: {datastore}. "
                f"Try one of the following: llama, elasticsearch, pinecone, weaviate, milvus, zilliz, redis, azuresearch, or qdrant"
            )
