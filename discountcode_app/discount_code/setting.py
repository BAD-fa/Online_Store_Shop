from pathlib import Path
from dotenv import find_dotenv,load_dotenv
from bson import ObjectId
import os
import pika
import pymongo


BASE_DIR = Path(__file__).resolve().parent.parent

env_file = Path(find_dotenv(usecwd=True))
load_dotenv(verbose=True, dotenv_path=env_file)
client = pymongo.MongoClient(host=os.environ.get("MONGO_HOST"))
db = client.discount_code

rabbit_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get("RABIT_HOST")))

api_url = os.environ.get("API_URL")

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")