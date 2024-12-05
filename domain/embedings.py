# import google.generativeai as genai
# import os
#
# os.environ['API_KEY'] ="AIzaSyAnieJXGl4LwvnmD1WCCZz8eOBAtthX39I"
# genai.configure(api_key=os.environ["API_KEY"])
#
# # Function to embed incoming text.
# def embed(content):
#     return genai.embed_content(
#         model="models/text-embedding-004",
#         task_type="RETRIEVAL_DOCUMENT",
#         content = content)

from langchain_google_vertexai import VertexAIEmbeddings

embeddings = VertexAIEmbeddings(model="text-embedding-004")
# embeddings.embed_query("Hello, world!")
print(embeddings.embed_query("Hello, world!"))

