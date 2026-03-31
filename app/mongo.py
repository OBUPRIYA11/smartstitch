from pymongo import MongoClient

from app.config import settings

client = MongoClient(settings.mongo_url)
db = client[settings.mongo_db]
model_collection = db["generated_models"]
