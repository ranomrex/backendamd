"""Small FastAPI service. Run with: uvicorn src.main:app --reload"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/item/{item_id}")
def get_item(item_id: int):
    return {"itemNo": item_id}
