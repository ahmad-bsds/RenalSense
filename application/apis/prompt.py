# api/api3.py
from fastapi import Depends
from utils import create_api, get_api_key

app = create_api()

@app.get("/prompt", dependencies=[Depends(get_api_key)])
def read_api3():
    return {"message": "This is API 3"}
