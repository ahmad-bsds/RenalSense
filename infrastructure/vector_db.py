# import fastembed
from pinecone import Pinecone
import os
from project_utils import get_logger, load_env_variable


logger = get_logger(__name__)

# Access the API key
# qd_api_key = os.getenv('QDRANT_API_KEY')
pc_api_key = load_env_variable("PINECONE_API_KEY", "../.env")#sample api key, will be removed.

# Initiating qdrant client.
pinecone_client = Pinecone(api_key=pc_api_key)

if pinecone_client:
    logger.info(f"Qdrant initiated! {pinecone_client}")
else:
    logger.info("Qdrant initiating failed.")



# TODO: add an api key in embeddings.py file.
# TODO: Use any technique to get Data in app.py in json formate


def add_collection_data(user_id: str, docs, ids, metadata=None):
    """Collection to add new Data into the collection by user id against related collection."""
    index = pinecone_client.Index(name=user_id)

    logger.info("Adding Data into vector DB...")

    pinecone_client.add(
        collection_name=user_id,
        documents=docs,
        metadata=metadata,
        ids=ids
    )
    logger.info("Data added successfully into vector database!")


def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    logger.info(f"Deleting qdrant collection {user_id}")
    pinecone_client.delete_collection(f"{user_id}")
    logger.info(f"Collection {user_id} deleted successfully!")


def query_collection(user_id, prompt):
    logger.info(f"Querying from {user_id}.......")
    query =  pinecone_client.query(
        collection_name=user_id,
        query_text=prompt,
        limit=10
    )
    if query:
        logger.info(f"Data query successful!")
    else:
        logger.info("Data query un-successful!")

    return query

# ------------
