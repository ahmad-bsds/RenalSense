from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

API_KEY = "123"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In-memory storage for demonstration purposes
data_storage: Dict[int, str] = {}
prompt_storage: Dict[int, str] = {}
inference_storage: Dict[int, str] = {
    0:"Your kidney is healthy."
}

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")

class DataItem(BaseModel):
    id: int
    data: str

class PromptItem(BaseModel):
    id: int
    prompt: str

class InferenceItem(BaseModel):
    id: int
    inference: str

@app.post("/data")
async def store_data(item: DataItem, api_key: APIKey = Depends(get_api_key)):
    data_storage[item.id] = item.data
    return {"message": "Data stored successfully"}

@app.post("/prompt")
async def store_prompt(item: PromptItem, api_key: APIKey = Depends(get_api_key)):
    prompt_storage[item.id] = item.prompt
    return {"message": "Prompt stored successfully"}

@app.get("/inference/{id}")
async def get_inference(id: int, api_key: APIKey = Depends(get_api_key)):
    if id not in inference_storage:
        raise HTTPException(status_code=404, detail="Inference not found")
    return {"id": id, "inference": inference_storage[id]}


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app)

# if __name__ == "__main__":
#     from gunicorn.app.wsgiapp import run
#     run()
