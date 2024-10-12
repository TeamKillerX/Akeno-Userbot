from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["Akeno"]
prefixes_collection = db["prefixes"]

async def create_index():
    await prefixes_collection.create_index("user_id", unique=True)

async def set_prefix_in_db(user_id: int, prefix: str):
    await prefixes_collection.update_one(
        {"user_id": user_id},
        {"$set": {"prefix": prefix}},
        upsert=True
    )

async def get_prefix(user_id: int):
    result = await prefixes_collection.find_one({"user_id": user_id})
    if result:
        return result["prefix"]
    else:
        return None
