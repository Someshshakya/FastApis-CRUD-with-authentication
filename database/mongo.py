from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
try:
    client = AsyncIOMotorClient(MONGO_URI)
    # Verify the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

db = client["fastapi_db"]
product_collection = db["products"]
customer_collection = db['customers']
