from motor.motor_asyncio import AsyncIOMotorClient
from app.settings.config import settings

client = AsyncIOMotorClient(settings.mongo_db_url)
db = client.investment_funds