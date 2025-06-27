from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client["fastapi_db"]
customer_collection = db["customers"]

def get_db():
    return db
