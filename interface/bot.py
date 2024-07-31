import openai
from langchain.prompts import ChatPromptTemplate
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

template_string = """Lets you are a kidney doctor and provide me answer of {prompt} from \
{data}. The answer must be simple, to the point, concise and true.
"""

# Defining template.
prompt_template = ChatPromptTemplate.from_template(template_string)


def inference(similarity_data, user_prompt):
    message = prompt_template.format_messages(
        data=similarity_data,
        prompt=user_prompt
    )

    response = chat(message)

    return response.content
