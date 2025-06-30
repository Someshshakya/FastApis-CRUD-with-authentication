import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NTEzMDM5NDd9.5oHljYwgs7JtY2keb6pLFZHENF0poRkbbt3GPOuOzIU"

'''This *test_creat_product* is used for testing the create product routes if its working or not in the 
it should work 
'''
@pytest.mark.asyncio
async def test_create_product(async_client):
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

# this is used to test out update product api 
@pytest.mark.asyncio
async def test_update_product(async_client):
    # Step 1: Create a product to update
    create_response = await async_client.post(
        "/product/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "TestProduct",
            "price": 100.0,
            "in_stock": True
        }
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["_id"]  # or "id" depending on your API's response

    # Step 2: Update the product
    update_response = await async_client.patch(
        f"/product/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "UpdatedProduct",
            "price": 150.0,
            "in_stock": False
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "UpdatedProduct"
    assert data["price"] == 150.0
    assert data["in_stock"] is False

#get all products from the database based on skip and limit
@pytest.mark.asyncio
async def test_get_all_products(async_client):
    all_product_response = await async_client.get(
        "/product/?skip=1&limit=1",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert all_product_response.status_code == 200
    data = all_product_response.json()
    type(data['data']) == list


@pytest.mark.asyncio
async def test_delete_product(async_client):
    # Step 1: Create a product to delete
    create_response = await async_client.post(
        "/product/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "ProductToDelete",
            "price": 50.0,
            "in_stock": True
        }
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["_id"]  # or "id" depending on your API's response

    # Step 2: Delete the product
    delete_response = await async_client.delete(
        f"/product/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200 or delete_response.status_code == 204
    data = delete_response.json()
    assert data["status"] == "success"
    assert "deleted" in data["message"] or "success" in data["message"].lower()
