from infrastructure.vector_db import add_collection_data, query_collection
from domain.data_embed import data_encode
from domain.document_chunks import chunk_text


def add_data_or_usr(user_id: str, data):
    """
    This function will add the user if not available in the vector database against his/her user id.
    """
    # Adding user in vector db.
    # create_collection(user_id=user_id)

    # Chunking the data.
    chunks = chunk_text(data)

    ids = list(range(len(chunks)))

    # Storing data into qdrant.
    add_collection_data(user_id=user_id, ids=ids, docs=chunks)


def produce_prompt_inference(user_id: str, prompt: str):
    """
    When user will enter simple prompt it will answer to that.
    """
    return query_collection(user_id=user_id, prompt=prompt)


def produce_image_inference():
    """
    Any prompt with image will be handel here.
    Parent function will be look like.
    if scan_food:
        pass
    elseif scan report:
        pass
    """
    pass


def update_user_recommendations(user_id: str):
    pass
# -------------------------
