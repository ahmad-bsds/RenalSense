import json
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from project_utils import get_logger, load_env_variable
from infrastructure.vector_db import query_collection
from langchain_groq import ChatGroq

logger = get_logger(__name__)


def groq_api(model: str = "mixtral-8x7b-32768") -> ChatGroq:
    """
    Initializes the GROQ API client.
    Args:
        model (str): The model to use for the API.
    Returns:
        ChatGroq: An instance of the ChatGroq model.
    """
    try:
        llm = ChatGroq(
            temperature=0,
            groq_api_key=load_env_variable("GROQ_API_KEY", env_file_path=load_env_variable("GROQ_API_KEY", env_file_path="../.env")),
            model_name=model,
        )
        return llm
    except Exception as e:
        print(f"Error initializing GROQ API: {e}")
        raise

chat = groq_api(model="mixtral-8x7b-32768")

template_string = """Lets you are a kidney doctor and provide me answer of {prompt} from \
{data}. The answer must be simple, to the point, concise and true.
"""

# Defining template.
inference_prompt_template = ChatPromptTemplate.from_template(template_string)


def inference(similarity_data, user_prompt):
    """This function will be used for inference purposes."""
    try:
        message = inference_prompt_template.format_messages(
        data=similarity_data,
        prompt=user_prompt )
    except Exception as e:
        raise logger.error("Error in inference! check inference in bt.py.!", e)

    response = chat(message)
    logger.info("Response created for inference.")

    return response.content


prompt_template = ChatPromptTemplate.from_template(
"""
Your task is to understand this {Data} and provide me kidney health insights and recommendations.\
Requirements:
- Answer must be a complete Json formate, with aggregated keys int(stage(0-5)), str(risk(High-Medium-Low-No)) and recommendations.
- Ensure that Json output is complete and well formatted.
- Act like a kidney doctor.
- Answer after a huge research, medical inference and understanding logic of Data and potential things.
- Be concise, be true.
- Do not Hallucinate.
- Don't make any hypothetical answer, give genuine answers.
- Output must be Json and nothing else.
"""
)

def health_updates(user_id):
    """This function will produce the condition of kidney health and related recommendations."""
    prompt = "My health Data"

    def similarity_data_() :
        """Function to retrieve relevant health Data."""
        logger.info("""Retrieving Data from pinecone...""")
        srh_r = query_collection(user_id=user_id, prompt=prompt)
        logger.info(f"Data query successful for health updates. {srh_r}")
        if srh_r:
            return srh_r
        else:
            logger.error(f"Qdrant Data Querying failed for health updates. {srh_r}")
            return {
                'stage': None,
                'risk': None,
                'recommendations': ['Error loading recommendations']
            }


    chain = prompt_template | chat
    response = chain.invoke({"Data": similarity_data_()}).content
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
