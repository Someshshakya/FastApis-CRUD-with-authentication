# test/conftest.py or inside your test file

import pytest
import sys
import os
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import pytest_asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # your FastAPI app
from database.mongo import get_db

MONGO_TEST_URL = "mongodb://localhost:27017"

# Override get_database
async def override_get_database() -> Database:
    client = AsyncIOMotorClient(MONGO_TEST_URL)
    test_db = client["test_fastapi_db"]
    customer_collection = test_db["customers"]
    return test_db

app.dependency_overrides[get_db] = override_get_database

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
