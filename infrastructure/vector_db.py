# import fastembed
from qdrant_client import QdrantClient, models

# Initiating qdrant client.
qdrant_client = QdrantClient(
    url="https://cd5dba88-8077-4aa3-9e35-78fd82a4a850.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="9Yt6Xfds2O-84IT8LwFVl3i0Ly8DRFZD7AGr1SrhABJDBF-VqaHZ3g",
)

def create_collection(user_id: str):
    """Function to create a collection against a user by user id."""
    return qdrant_client.create_collection(
        collection_name=f"{user_id}",
        vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
    )

# TODO: how to vector set size.
def add_collection_data(user_id: str, ids, vectors):
    """Collection to add new data into the collection by user id against related collection."""
    qdrant_client.upsert(
        collection_name= user_id,
        points= models.Batch(
            ids = None,
            vectors= None
        )
    )

def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    qdrant_client.delete_collection(collection_name=f"{user_id}")

def query_collection(user_id: str, query: str):
    """Function to query the collection by user id for relative collection and the query test."""
    qdrant_client.query(collection_name = user_id, query_text= query)