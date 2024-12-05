import os
from together import Together
from project_utils import load_env_variable

client = Together(api_key=load_env_variable("TOGETHER_API_KEY", "../.env"))

def embed(text):
  response = client.embeddings.create(
    model = "togethercomputer/m2-bert-80M-8k-retrieval",
    input = text
  )

  return response.data[0].embedding

# print(embed("Our solar system orbits the Milky Way galaxy at about 515,000 mph"))