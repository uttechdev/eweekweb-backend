import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()
orgs_global = {}

@asynccontextmanager
async def mongo_client():
    uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(uri)
    try:
        yield client
    finally:
        client.close()