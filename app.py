from pymongo.mongo_client import MongoClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import tinder_library as TL
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str | None

class Number(BaseModel):
    number: int | None

client, primesDB, users = None, None, None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global users, primesDB, client
    username, password = TL.get_mongo_credentials("secrets.txt")
    uri = f"mongodb+srv://{username}:{password}@cluster0.6ug28qa.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    primesDB = client["primesDB"]
    users = primesDB["users"]

    yield

    client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return "Health Ok"

@app.get("/user")
async def get_user_info(username:str):
    return JSONResponse(content=users.find_one({"key":username}, {'_id': False}), status_code=200)

@app.post("/user")
async def signup(user:User):
    if not users.find_one({"key":user.username}) != None:
        users.insert_one({"key":user.username, 
                          "value":{"password":"this is a test dont store passwords in plain text"}})
        return "User Signed Up"
    else:
        return "User Already Signed Up"
    
@app.post("/number")
async def generate_number(user:User, number:Number):
    record_insert = {"$set":{"number": 5}}
    users.update_one({"key":user.username}, record_insert)
    return {"message":"Number added to user", "number": 5}

@app.delete("/number")
async def clear_numbers():
    users.update_many({}, {"$unset": {"number": ""}})
    return JSONResponse(content={"message":"Deleted Properly"}, status_code=200)