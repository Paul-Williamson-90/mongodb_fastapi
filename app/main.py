from fastapi import FastAPI
from pymongo import MongoClient
import json

app = FastAPI()

client = MongoClient("mongodb://db:27017/")
db = client["demo_db"]
collection = db["demo_collection"]

@app.get("/ping/")
async def ping():
    return {"message": "pong"}

@app.post("/post/")
async def post_data(data: dict):
    try:
        inputs = data.get("data")
        if isinstance(inputs, list):
            collection.insert_many(inputs)
        else:
            collection.insert_one(inputs)
        
        return {"message": "Data inserted successfully"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/get_all_data/")
async def get_all_data():
    try:
        data = list(collection.find())
        for item in data:
            item["_id"] = str(item["_id"])
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/get_data/{key}/{value}")
async def get_data(key: str, value: str):
    try:
        data = list(collection.find({key: value}))
        for item in data:
            item["_id"] = str(item["_id"])
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}