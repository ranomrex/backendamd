from fastapi import FastAPI

app=FastAPI()
@app.get("/")
def home():
    return {"message": "Hellow World"}

@app.get("/item/{item_id}")
def fun(item_id: int):
    return {"itemNo": item_id}