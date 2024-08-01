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

template_string = """
Your task is to generate value-able insights from {data}.\
Here are some of output requirements:
-Be act like a special doctor with valuable experience and casual research experience.
-Generate insights in summary form.
-Be simple and concise
-Research well before explaining and generating insights.
-Don't write irrelevant.
-Write in a way that data needs to be embed and search latter so keep the formate accordingly.
-Don't use personal info such as: "name, medical record number, date of report however use age for logical research and\
insights building."
"""

# Defining template.
prompt_template = ChatPromptTemplate.from_template(template_string)


def enhance_data(data):
    message = prompt_template.format_messages(
        data=data
    )

    response = chat(message)
    return response.content