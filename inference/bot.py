import json
import openai
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from utils import get_logger
from infrastructure.vector_db import query_collection

logger = get_logger(__name__)

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
    logger.info("Response created for inference.")

    return response.content


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
        if srh_r:
            search = ""
            n = len(srh_r)
            for i in range(n):
                search += (srh_r[i].metadata['document'])
            return str(search)
        else:
            logger.error(f"Qdrant Data Querying failed for health updates. {srh_r}")
            return {
                'stage': None,
                'risk': None,
                'recommendations': ['Error loading recommendations']
            }



    chain = prompt_template | chat
    response = chain.invoke({"data": similarity_data_()}).content
    # logger.info("Response successful for health updates.")

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
            logger.info(f"Json successful {json_data}")
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {e}")
    else:
        logger.info("No valid JSON found.")

    # If there is error.
    return {
                  'stage': None,
                  'risk': None,
                  'recommendations': ['Error loading recommendations']
                }



# print(health_updates("97148076364870717344591996034064565110"))
