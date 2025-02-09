from motor.motor_asyncio import AsyncIOMotorClient

from app.config import config

client = AsyncIOMotorClient(config.MONGO_URI)
pdf_collection = client[config.DATABASE_NAME][config.PDF_COLLECTION]
result_collection = client[config.DATABASE_NAME][config.RESULT_COLLECTION]
