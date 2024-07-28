import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
# Load the environment variables from the .env file at the specified path
load_dotenv(dotenv_path='../.env')

# Access the API key
fa_api_key = os.getenv('FALCON_API_KEY')

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = fa_api_key

chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    streaming=True,
)

# Simple invocation:
print(
    chat.invoke(
        [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content="Hello!"),
        ]
    )
)

# Streaming invocation:
for chunk in chat.stream("Write two words you most like."):
    print(chunk.content, end="", flush=True)