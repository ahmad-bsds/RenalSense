from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import Dict
from domain.user_functions import add_data_or_usr, produce_prompt_inference

app = FastAPI()

API_KEY = "123"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In-memory storage for demonstration purposes
data_storage: Dict[str, str] = {}
prompt_storage: Dict[str, str] = {}
inference_storage: Dict[str, str] = {
    '0': "Your kidney is healthy."
}


async def get_api_key(api_key_headers: str = Security(api_key_header)):
    if api_key_headers == API_KEY:
        return api_key_headers
    raise HTTPException(status_code=403, detail="Could not validate credentials")


class DataItem(BaseModel):
    id: str
    data: str


class PromptItem(BaseModel):
    id: str
    prompt: str


class InferenceItem(BaseModel):
    id: str
    prompt: str


@app.post("/data")
async def store_data(item: DataItem, api_key: APIKey = Depends(get_api_key)):
    add_data_or_usr(user_id=item.id, data=item.data)
    print("Data sent successful!")


@app.post("/prompt")
async def store_prompt(item: PromptItem, api_key: APIKey = Depends(get_api_key)):
    prompt_storage[item.id] = item.prompt
    return {"message": "Prompt stored successfully"}


@app.get("/inference/{id}")
async def get_inference(item: InferenceItem, api_key: APIKey = Depends(get_api_key)):
    if item not in inference_storage:
        raise HTTPException(status_code=404, detail="Inference not found")
    return produce_prompt_inference(user_id=item.id, prompt=item.prompt)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

