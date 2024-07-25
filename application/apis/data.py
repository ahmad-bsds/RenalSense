# first 
from fastapi import Depends
from utils import create_api, get_api_key

app = create_api()

@app.get("/data", dependencies=[Depends(get_api_key)])
def read_api1():
    return {"message": "This is API 1"}
