from fastapi import FastAPI
from models import session


app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.get("/health")
async def return_health():
    return {"status": "ok"}

