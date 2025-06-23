from fastapi import APIRouter, HTTPException, status, Body, Depends, Header,Query
from models.product import Product, ProductInDB, PaginatedProductResponse
from database.mongo import product_collection
from exceptions import NotFoundException, BadRequestException, DatabaseException
from bson import ObjectId
import logging
from typing import Optional
from pydantic import BaseModel
from dependencies import require_role

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Update Product Schema
class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Mobile",
                "price": 899.99,
                "in_stock": True
            }
        }

# Helper converts mongo object Id to string 

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "in_stock": product.get("in_stock", True)
    }

#create a product

@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product,user=Depends(require_role(["admin","store"]))):
    try:
        logger.info(f"Received product data: {product.model_dump()}")
        
        # Convert Pydantic model to dict
        product_dict = product.model_dump()
        logger.info(f"Converted to dict: {product_dict}")
        
        # Insert the product
        result = await product_collection.insert_one(product_dict)
        logger.info(f"Insert result: {result.inserted_id}")
        
        # Fetch the created product
        created_product = await product_collection.find_one({"_id": result.inserted_id})
        if not created_product:
            logger.error("Failed to retrieve created product")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created product"
            )
        
        logger.info(f"Created product: {created_product}")
        
        # Create response model
        response = ProductInDB(
            _id=created_product["_id"],
            name=created_product["name"],
            price=created_product["price"],
            in_stock=created_product.get("in_stock", True)
        )
        logger.info(f"Response model: {response.model_dump()}")
        return response
        
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


#update product
# @router.patch("/{product_id}", response_model=ProductInDB)
# async def update_product(
#     product_id: str,
#     data: UpdateProduct = Body(
#         ...,
#         example={
#             "name": "Updated Mobile",
#             "price": 899.99,
#             "in_stock": True
#         }
#     ),
#     user=Depends(require_role(["admin","store"]))
# ):
#     try:
#         logger.info(f"Updating product {product_id} with data: {data.model_dump(exclude_unset=True)}")
        
#         # Validate ObjectId
#         if not ObjectId.is_valid(product_id):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid product ID format. Please provide a valid MongoDB ObjectId"
#             )

#         # Convert Pydantic model to dict, excluding unset fields
#         update_data = data.model_dump(exclude_unset=True)
#         if not update_data:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="No valid fields to update. Please provide at least one field to update"
#             )
        
#         # Update the product
#         result = await product_collection.update_one(
#             {"_id": ObjectId(product_id)},
#             {"$set": update_data}
#         )
        
#         if result.matched_count == 0:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Product with ID {product_id} not found"
#             )
            
#         if result.modified_count == 0:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="No changes made to the product. The provided values are the same as existing values"
#             )
        
#         # Fetch updated product
#         updated_product = await product_collection.find_one({"_id": ObjectId(product_id)})
#         if not updated_product:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Product not found after update"
#             )
            
#         # Return updated product
#         return ProductInDB(
#             _id=updated_product["_id"],
#             name=updated_product["name"],
#             price=updated_product["price"],
#             in_stock=updated_product.get("in_stock", True)
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error updating product: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error updating product: {str(e)}"
#         )
# update with expection handling with built-in
@router.patch("/{product_id}", response_model=ProductInDB)
async def update_product(
    product_id: str,
    data: UpdateProduct = Body(...),
    user=Depends(require_role(["admin","store"]))
):
    try:
        logger.info(f"Updating product {product_id} with data: {data.model_dump(exclude_unset=True)}")
        
        if not ObjectId.is_valid(product_id):
            raise BadRequestException("Invalid product ID format. Please provide a valid MongoDB ObjectId")

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields to update. Please provide at least one field")

        result = await product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise NotFoundException(f"Product with ID {product_id} not found")

        if result.modified_count == 0:
            raise BadRequestException("No changes made to the product")

        updated_product = await product_collection.find_one({"_id": ObjectId(product_id)})
        if not updated_product:
            raise NotFoundException("Product not found after update")

        return ProductInDB(
            _id=updated_product["_id"],
            name=updated_product["name"],
            price=updated_product["price"],
            in_stock=updated_product.get("in_stock", True)
        )
    
    except (BadRequestException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise DatabaseException(str(e))
#get all products
@router.get("/", response_model=PaginatedProductResponse)
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    user=Depends(require_role(["admin", "user"]))
):
    try:
        cursor = product_collection.find({}).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)

        response = [
            ProductInDB(**product).model_dump(by_alias=True)
            for product in products
        ]

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found"
            )

        total = await product_collection.count_documents({})

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": response
        }

    except Exception as e:
        logger.error(f"Error while getting the products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while getting products: {str(e)}"
        )


#delete product
@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    user=Depends(require_role(["admin"]))
):
    try:
        result = await product_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"status": "success", "message": "Product deleted"}
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting product: {str(e)}"
        )

