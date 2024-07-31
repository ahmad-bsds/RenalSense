from domain.user_functions import add_new_user_in_app, add_user_data, produce_prompt_inference
from domain.prompt_embed import prompt_encode
from infrastructure.vector_db import qdrant_client
from infrastructure.vector_db import search

data = """
The rapid advancement of artificial intelligence has led to significant breakthroughs in various fields.\
 From autonomous vehicles navigating complex urban environments to sophisticated medical diagnosis systems \
 aiding in disease detection, AI's potential to revolutionize our lives is immense. As AI continues to evolve,\
  it is crucial to address ethical considerations and ensure responsible development to harness\
   its benefits while mitigating potential risks
"""
prompt = "What are the potential risks associated with the advancement of artificial intelligence?"
USER_ID = "040"

print("....................Start")
add_new_user_in_app(user_id=USER_ID, data=data)
print("................................Done 1/2")
print(search(user_id=USER_ID, prompt=prompt))
print("................................ Done 2/2")
print(qdrant_client.get_collection(collection_name=USER_ID))
