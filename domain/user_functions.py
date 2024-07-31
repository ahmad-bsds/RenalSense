from infrastructure.vector_db import create_collection, add_collection_data, query_collection
from domain.data_embed import data_encode
from domain.document_chunks import chunk_text


def add_new_user_in_app(user_id: str, data):
    """
    This function will add the user in the vector database against his/her user id.
    """
    # Adding user in vector db.
    create_collection(user_id=user_id)

    # Chunking the data.
    chunks = chunk_text(data)

    # Encoding data into vectors.
    encoded_data = data_encode(chunks)

    idx = list(range(len(encoded_data)))

    # Storing data into qdrant.
    add_collection_data(user_id=user_id, ids=idx, vectors=encoded_data.tolist())


def add_user_data(user_id: str, data):
    """
    This function will add the user data in the vector database against his/her user id.
    """
    # Chunking the data.
    chunks = chunk_text(data)

    # Encoding data into vectors.
    encoded_data = data_encode(chunks)

    # Storing data into qdrant.
    for ids, vec in enumerate(encoded_data):
        # Adding his/her encoded data in vector DB.
        add_collection_data(user_id=user_id, ids=ids, vectors=vec)


def produce_prompt_inference(user_id: str, prompt: str):
    """
    When user will enter simple prompt it will answer to that.
    """
    return query_collection(user_id=user_id, query=prompt)


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
