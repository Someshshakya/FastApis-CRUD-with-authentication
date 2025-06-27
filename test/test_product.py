import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

@pytest.mark.asyncio
async def test_create_product(async_client):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NTA5NDIxNTB9.-Uv0xNMW96smmSZ97wSGH8l0lj6AQQXQBB9piT5sAbU"
    response = await async_client.post(
        "/product/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "phone",
            "price": 199.99,
            "in_stock": True
        }
    )
    print(f"this is testing response {response}")
    assert response.status_code == 201
    assert response.json()["name"] == "phone"
