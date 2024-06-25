from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

password = os.getenv("MONGODB_PASSWORD")
user = os.getenv("MONGODB_USER")

client = MongoClient(
    f"mongodb+srv://{user}:{password}@cluster0.x5etwlt.mongodb.net/").test

