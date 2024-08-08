import openai
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from infrastructure.vector_db import query_collection

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
    max_tokens=50,
    temperature=0
)

template_string = """Lets you are a kidney doctor and provide me answer of {prompt} from \
{data}. The answer must be simple, to the point, concise and true.
"""

# Defining template.
inference_prompt_template = ChatPromptTemplate.from_template(template_string)


def inference(similarity_data, user_prompt):
    """This function will be used for inference purposes."""
    message = inference_prompt_template.format_messages(
        data=similarity_data,
        prompt=user_prompt
    )

    response = chat(message)

    return response.content


health_update_template_string = """
Your task is to understand this {data} and provide me kidney health insights and recommendations.\
FORMATE OF OUTPUT:
Insights:
Stage: x
Type of kidney disease: this is your kidney disease.
---------------------------------------------------------
Recommendations:
Here are recommendations based on data provided.

Requirements:
- Act like a kidney doctor.
- Answer after a huge research, medical inference and under standing logic of data and potential things.
- Be concise, be true.
- If you dont have answer write NULL.
- If there is no stage or disease write --
- Don't make any hypothetical answer, give genuine answers.
"""

health_updates_prompt_template = ChatPromptTemplate.from_template(health_update_template_string)


def health_updates(user_id):
    """This function will produce the condition of kidney health and related recommendations."""
    prompt = "My health data"

    def similarity_data_():
        srh_r = query_collection(user_id=user_id, prompt=prompt)
        search = ""
        n = len(srh_r)
        for i in range(n):
            search += (srh_r[i].metadata['document'])
        return search

    message = health_updates_prompt_template.format_messages(
        data=similarity_data_()
    )

    response = chat(message)

    return response.content
