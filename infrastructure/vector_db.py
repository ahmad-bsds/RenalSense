# import fastembed
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
import os

# Load the environment variables from the .env file at the specified path
load_dotenv(dotenv_path='../.env')

# Access the API key
qd_api_key = os.getenv('QDRANT_API_KEY')

# Initiating qdrant client.
qdrant_client = QdrantClient(
    url="https://09242a5b-7cf2-4398-9e78-88478b9f1f4f.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=qd_api_key,
)


def create_collection(user_id: str):
    """Function to create a collection against a user by user id."""
    return qdrant_client.create_collection(
        collection_name=f"{user_id}",
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )


# TODO: how to vector set size.
def add_collection_data(user_id: str, ids, vectors):
    """Collection to add new data into the collection by user id against related collection."""
    qdrant_client.upsert(
        collection_name=user_id,
        points=models.Batch(
            ids=ids,
            vectors=vectors
        )
    )


def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    qdrant_client.delete_collection(collection_name=f"{user_id}")


def query_collection(user_id: str, query: str):
    """Function to query the collection by user id for relative collection and the query test."""
    qdrant_client.query(collection_name=user_id, query_text=query, limit=3)


def search(vect, c_name):
    return qdrant_client.search(
        collection_name=c_name,
        query_vector=vect
    )
