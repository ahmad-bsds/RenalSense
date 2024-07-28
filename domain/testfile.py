from ..infrastructure.vector_db import create_collection, add_collection_data

def add_new_user_in_app(user_id: str, ids, vectors):
    """
    This function will add the user in the vector database against his/her user id.
    """
    # Adding user in vector db.
    create_collection(user_id=user_id)
    # Adding his/her data in vector DB.
    add_collection_data(user_id=user_id, ids=ids, vectors=vectors)

def add_new_user_data(user_id: str, ids, vectors):
    """
    This function will add the user data in the vector database against his/her user id.
    """
    # Adding his/her data in vector DB.
    add_collection_data(user_id=user_id, ids=ids, vectors=vectors)

def produce_prompt_inference():
    """
    When user will enter simple prompt it will answer to that.
    """
    pass

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