from fastapi import APIRouter, HTTPException, status, Body
from typing import Optional
import logging
from models.customer import Customer, CustomerInDB
from database.mongo import customer_collection
from auth import create_access_token
from models.auth import UserLogin
from fastapi import Depends


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

#create user 

@router.post("/user",response_model=CustomerInDB, status_code=status.HTTP_201_CREATED)
async def sign_up_user(user: Customer):
  try:
    data_to_store = user.model_dump()
    # Validate role and role_text combination
    valid_roles = [
         "user",
         "admin",
         "store"
    ]
    logger.info(f"data_to_store {data_to_store}")
    if data_to_store["role"] not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role and role_text combination. Use: (1, 'user'), (2, 'admin'), (3, 'store')"
        )
    # first check not user found with email and phone 
    is_email_exists = await customer_collection.find_one({"email":data_to_store["email"]},{"email":1})
    if is_email_exists and is_email_exists["email"] == data_to_store["email"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Please try with other email."
        )

    result = await customer_collection.insert_one(data_to_store)

    # Fetch the created product
    created_customer = await customer_collection.find_one({"_id": result.inserted_id})
    if not created_customer:
        logger.error("Failed to retrieve created user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created user"
        )
    
    logger.info(f"Created user: {created_customer}")
    
    # Create response model
    response = CustomerInDB(
        _id=created_customer["_id"],
        first_name=created_customer["first_name"],
        last_name=created_customer["last_name"],
        email=created_customer["email"],
        phone=created_customer["phone"],
        country_code=created_customer["country_code"],
        password=created_customer["password"],
        role=created_customer["role"],
    )
    logger.info(f"Response model: {response.model_dump()}")
    return response
    
  except Exception as e:
    logger.error(f"Error creating user: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error creating user: {str(e)}"
    )


@router.post("/login/customer")
async def login_customer(user: UserLogin = Body(...)):
    db_user = await customer_collection.find_one({"email": user.username})
    if not db_user or db_user.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if db_user.get("role") != "user":
        raise HTTPException(status_code=403, detail="Not a customer account")
    token = create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login/admin")
async def login_admin(user: UserLogin = Body(...)):
    db_user = await customer_collection.find_one({"email": user.username})
    if not db_user or db_user.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if db_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not an admin account")
    token = create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login/store")
async def login_store(user: UserLogin = Body(...)):
    db_user = await customer_collection.find_one({"email": user.username})
    if not db_user or db_user.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if db_user.get("role") != "store":
        raise HTTPException(status_code=403, detail="Not a store account")
    token = create_access_token({"sub": db_user["email"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}