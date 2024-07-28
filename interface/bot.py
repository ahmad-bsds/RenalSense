import openai
from dotenv import load_dotenv
import os
# Load the environment variables from the .env file at the specified path
load_dotenv(dotenv_path='../.env')

# Access the API key
fa_api_key = os.getenv('FALCON_API_KEY')

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = fa_api_key

client = openai.OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

# Simple invocation:
print(client.chat.completions.create(
    model="tiiuae/falcon-11b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
))

# Streaming invocation:
for chunk in client.chat.completions.create(
    messages=[{
      "role": "user",
      "content": "Write two words you like the most."
    }],
    model="tiiuae/falcon-11b",
    stream=True,
):
    delta_content = chunk.choices[0].delta.content
    if delta_content:
        print(delta_content, sep="", end="", flush=True)