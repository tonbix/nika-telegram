from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from configparser import ConfigParser

load_dotenv()

async def setup_db():
    config = ConfigParser()
    config.read("config.ini")
    
    MONGO_HOST = "localhost"
    MONGO_DB = config.get("Database", "Name")
    MONGO_PASS=getenv("MONGO_PASS")
    
    print(f"using \"{MONGO_DB}\" database")

    client = MongoClient(f"mongodb://tonbix:{MONGO_PASS}@{MONGO_HOST}:27017/{MONGO_DB}?authSource=admin")
    db = client[MONGO_DB]

    return (client, db)
