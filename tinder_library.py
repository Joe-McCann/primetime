from pymongo.mongo_client import MongoClient

def get_mongo_credentials(filename):
    with open(filename, 'r') as file:
        username = file.readline().strip()
        password = file.readline().strip()
    return username, password

def check_user_exists(collection, username):
    return collection.find_one({"key":username}) != None

def sign_user_up(collection, username):
    try:
        collection.insert_one({"key":username, "value":{"password":"this is a test dont store passwords in plain text"}})
    except:
        return False