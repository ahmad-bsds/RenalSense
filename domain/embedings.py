import os
from together import Together
from project_utils import load_env_variable, get_logger

logger = get_logger(__name__)

print(load_env_variable("TOGETHER_API_KEY", "../.env"))

client = Together(api_key=load_env_variable("TOGETHER_API_KEY", "./.env"))

def embed(text):

  try:
    response = client.embeddings.create(
      model = "togethercomputer/m2-bert-80M-8k-retrieval",
      input = str(text)
    )

  except Exception as e:
    raise logger.error("Error generating embeddings.", e)

  return response.data[0].embedding

# print(embed("Our solar system orbits the Milky Way galaxy at about 515,000 mph"))