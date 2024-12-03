# import fastembed
from qdrant_client import QdrantClient, models
import o
from utils import get_logger, load_env_variable


logger = get_logger(__name__)

# Access the API key
# qd_api_key = os.getenv('QDRANT_API_KEY')
qd_api_key = load_env_variable("QDRANT_API_KEY", "../.env")#sample api key, will be removed.

# Initiating qdrant client.
qdrant_client = QdrantClient(
    url=load_env_variable("QDRANT_URL", "../.env"),
    api_key=qd_api_key,
)

if qdrant_client:
    logger.info(f"Qdrant initiated! {qdrant_client}")
else:
    logger.info("Qdrant initiating failed.")


def add_collection_data(user_id: str, docs, ids, metadata=None):
    """Collection to add new data into the collection by user id against related collection."""
    logger.info("Adding data into vector DB...")
    return qdrant_client.add(
        collection_name=user_id,
        documents=docs,
        metadata=metadata,
        ids=ids
    )


def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    logger.info(f"Deleting qdrant collection {user_id}")
    return qdrant_client.delete_collection(collection_name=f"{user_id}")


def query_collection(user_id, prompt):
    logger.info(f"Querying from {user_id}.......")
    query =  qdrant_client.query(
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
