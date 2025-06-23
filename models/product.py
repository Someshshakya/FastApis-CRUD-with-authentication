from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue, GetJsonSchemaHandler


# ✅ Custom PyObjectId for Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate)
                ])
            ])
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "description": "MongoDB ObjectId"}


# ✅ Base Product schema (request body)
class Product(BaseModel):
    name: str = Field(..., example="Laptop")
    price: float = Field(..., example=999.99)
    in_stock: bool = Field(default=True, example=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "in_stock": True
            }
        }

# # updateProduct 
# class UpdateProduct(BaseModel):
#     product_id: str =  Field(...,example="682b083c1765cf0f011e330d")
#     name: Optional[str] = Field(None, example="Laptop")
#     price: Optional[float] = Field(None, example=999.99)
#     in_stock: Optional[bool] = Field(None, example=True)

#     class Config:
#             json_schema_extra = {
#                 "example": {
#                     "product_id":"682b083c1765cf0f011e330d",
#                     "name": "Laptop",
#                     "price": 999.99,
#                     "in_stock": True
#                 }
#             }


# ✅ Product with MongoDB _id (response from DB)
class ProductInDB(Product):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
class PaginatedProductResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[ProductInDB]
