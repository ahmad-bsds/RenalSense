import google.generativeai as genai
import os

os.environ['API_KEY'] ="AIzaSyCzd-Zikh2jDCQi4ASoJJYiTJ8AsSPNAU0"
genai.configure(api_key=os.environ["API_KEY"])

# Function to embed incoming text.
def embed(content):
    return genai.embed_content(
        model="models/text-embedding-004",
        task_type="RETRIEVAL_DOCUMENT",
        content = content
    )