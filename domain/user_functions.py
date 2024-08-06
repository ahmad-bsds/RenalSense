from infrastructure.vector_db import add_collection_data, query_collection
from domain.document_chunks import chunk_text
from inference.bot import inference


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
    srh_r = query_collection(user_id=user_id, prompt=prompt)
    search = ""
    n = len(srh_r)
    for i in range(n):
        search += (srh_r[i].metadata['document'])

    # Provide inference.
    inf = inference(search, prompt)
    return inf


def produce_image_inference(user_id, prompt):
    pass


def update_user_recommendations(user_id: str):
    pass
# -------------------------
