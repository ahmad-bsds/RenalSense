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


def add_collection_data(user_id: str, docs, ids):
    """Collection to add new data into the collection by user id against related collection."""
    qdrant_client.add(
        collection_name=user_id,
        documents=docs,
        # metadata=metadata,
        ids=ids
    )


def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    qdrant_client.delete_collection(collection_name=f"{user_id}")


def query_collection(user_id, prompt):
    return qdrant_client.query(
        collection_name=user_id,
        query_text=prompt
    )

# ------------
