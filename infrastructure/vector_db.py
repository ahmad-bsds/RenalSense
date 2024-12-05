# import fastembed
from pinecone import Pinecone
from domain.embedings import embed
import os
from project_utils import get_logger, load_env_variable
import json

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


def read_json_file(file_path):
  """Reads a JSON file and returns its contents as a Python object.

  Args:
    file_path: The path to the JSON file.

  Returns:
    The contents of the JSON file as a Python object (typically a dictionary or list).
  """

  with open(file_path, 'r') as f:
    data = json.load(f)
  return data

processed_data = []

def add_collection_data(metadata, user_id: str): # file: str= "./data.json"
    """Function will load data and process this data to store in a list. List will be stored in
        the vector database.
    """
    try:
        logger.info("Embeddings generating!")
        embeddings = embed(metadata)
        logger.info("Embeddings generated!")
    except Exception as e:
        raise logger.error(e)

    # insert processed data in the list.
    logger.info("Inserting data in the list!")

    processed_data.append(
        {
            "values": embeddings,
            "id": "0",
            "metadata": metadata
        }
    )
    logger.info("Data inserted in the list!")

    logger.info("Inserting data in the vector db!")
    collection_index = pinecone_client.Index("renal-sense")
    collection_index.upsert(vectors=processed_data, namespace=str(user_id))
    logger.info("Data inserted in the vector db!")



def delete_collection(user_id: str):
    """Function to delete the collection in case user delete his/her account"""
    logger.info(f"Deleting qdrant collection {user_id}")
    pinecone_client.delete_collection(f"{user_id}")
    logger.info(f"Collection {user_id} deleted successfully!")


def query_collection(user_id, prompt):
    # logger.info(f"Querying from {user_id}.......")
    # query =  pinecone_client.query(
    #     collection_name=user_id,
    #     query_text=prompt,
    #     limit=10
    # )
    # if query:
    #     logger.info(f"Data query successful!")
    # else:
    #     logger.info("Data query un-successful!")
    #
    # return query

    logger.info(f"Querying from {user_id}.......")
    collection_index = pinecone_client.Index("renal-sense")
    logger.info(f"Collection {user_id} initiated!")

    logger.info(f"Embeddings generating!")
    vector = embed(prompt)
    logger.info(f"Embeddings generated!")

    logger.info(f"Querying from {user_id}.......")
    response = collection_index.query(
        namespace=str(user_id),
        vector=vector,
        top_k=2,
        include_values=True,
        include_metadata=True,
    )
    logger.info(f"Data query successful!")

    try:
        return response["matches"][0]["metadata"]
    except Exception as e:
        logger.error("Error while querying data in vector database.", e)
        return "Sorry! I could not process your request. Please try again later."

# ------------
