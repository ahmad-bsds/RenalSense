import json

import openai
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.utils.openai_functions import convert_pydantic_to_openai_function
from dotenv import load_dotenv
import time
import os
from infrastructure.vector_db import query_collection
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

# Load the environment variables from the .env file at the specified path
load_dotenv(dotenv_path='../.env')

# Access the API key
fa_api_key = os.getenv('FALCON_API_KEY')
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = fa_api_key

# All of these APIs are just for representation purpose.
QDRANT_API_KEY = "Fbo3AybCrGPnWhP2KajA2e0so7_Mz313wleg10ESKFzBB73v5G3JZQ"
FALCON_API_KEY = "api71-api-95a38584-2219-4703-926a-250532246774"
os.environ.setdefault("OPENAI_API_KEY", FALCON_API_KEY)

chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    streaming=True,
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


# health_update_template_string = """
# Your task is to understand this {Your health is normal} and provide me kidney health insights and recommendations.\
# Your output must be a single list containing dictionaries, structured as follows:
# [
#     {
#         'stage': int(0-5),
#         'risk': str(High-Medium-Low)
#     },
#     {'icon': str(font awesome icon id), 'title': str,
#      'description': str},
#     {'icon': str(font awesome icon id), 'title': str, 'description': str},
#     {'icon': str(font awesome icon id), 'title': str,
#      'description': str}
# ]
# ---------------------------------------------------------
# Recommendations:
# Here are recommendations based on data provided.
#
# Requirements:
# - Act like a kidney doctor.
# - Answer after a huge research, medical inference and under standing logic of data and potential things.
# - Be concise, be true.
# - If you dont have answer write NULL.
# - If there is no stage or disease write --
# - Don't make any hypothetical answer, give genuine answers.
# """

prompt_template = ChatPromptTemplate.from_template(
"""
Your task is to understand this {data} and provide me kidney health insights and recommendations.\
Requirements:
- Answer must be a complete Json formate, with aggregated keys int(stage(0-5)), str(risk(High-Medium-Low-No)) and recommendations.
- Ensure that Json output is complete and well formatted.
- Act like a kidney doctor.
- Answer after a huge research, medical inference and understanding logic of data and potential things.
- Be concise, be true.
- Do not Hallucinate.
- Don't make any hypothetical answer, give genuine answers.
- Output must be Json and nothing else.
"""
)

def health_updates(user_id):
    """This function will produce the condition of kidney health and related recommendations."""
    prompt = "My health data"

    def similarity_data_() -> json:
        """Function to retrieve relevant health data."""
        srh_r = query_collection(user_id=user_id, prompt=prompt)
        search = ""
        n = len(srh_r)
        for i in range(n):
            search += (srh_r[i].metadata['document'])
        return str(search)

    chain = prompt_template | chat
    response = chain.invoke({"data": similarity_data_()}).content

    # Your malformed JSON string
    json_string = response

    # Find the last closing brace to isolate valid JSON
    last_brace_index = json_string.rfind("}")

    # If valid closing brace is found
    if last_brace_index != -1:
        valid_json_string = json_string[:last_brace_index + 1]

        try:
            # Parse the valid JSON
            json_data = json.loads(valid_json_string)
            print(json_data)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("No valid JSON found.")

    # If there is error.
    return {
                  'stage': None,
                  'risk': None,
                  'recommendations': ['Error loading recommendations']
                }



# print(health_updates("97148076364870717344591996034064565110"))
