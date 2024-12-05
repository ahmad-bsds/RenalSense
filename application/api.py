from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import Dict
from domain.user_functions import add_data_or_usr, produce_prompt_inference
from inference.bot import health_updates
from project_utils import get_logger

logger = get_logger(__name__)

fast_app = FastAPI()

API_KEY = "123"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_headers: str = Security(api_key_header)):
    if api_key_headers == API_KEY:
        return api_key_headers
    raise HTTPException(status_code=403, detail="Could not validate credentials")


class DataItem(BaseModel):
    id: str
    data: str


# API for handling users and their Data.
@fast_app.post("/Data")
async def store_data(item: DataItem, api_key: APIKey = Depends(get_api_key)):
    logger.info(f"User {item.id} is getting in........")
    add_data_or_usr(user_id=item.id, data=item.data) # id is user id and data is json file.
    return "Data sent successful!"


# API to give every user personalized updates.
@fast_app.post("/health_updates/{user_id}")
async def health_update(user_id, api_key: APIKey = Depends(get_api_key)):
    logger.info(f"User {user_id} is getting health updates........")
    return health_updates(user_id=user_id)


# API to get custom message inference.
@fast_app.get("/inference/{user_id}")
async def get_inference(user_id, prompt, api_key: APIKey = Depends(get_api_key)):
    logger.info(f"User {user_id} is getting inference........")
    return produce_prompt_inference(user_id=user_id, prompt=prompt)


if __name__ == "__main__":
     import uvicorn
     uvicorn.run(fast_app)