from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


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


class Customer(BaseModel):
    first_name: str = Field(...,example="Somesh")
    last_name: str = Field(...,example="Shakya")
    email: str = Field(...,example="somesh@email.com")
    phone: str = Field(...,example="8373738383")
    country_code:str = Field(...,example="+91")
    password: str = Field(..., example="password123")
    role: str = Field(..., example="customer", description="customer, admin, or store")
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "first_name": "Somesh",
                    "last_name": "Shakya",
                    "email": "somesh@gmail.com",
                    "phone": "8433432222",
                    "country_code": "+91",
                    "password": "password123",
                    "role": "customer"
                },
                {
                    "first_name": "Admin",
                    "last_name": "User",
                    "email": "admin@email.com",
                    "phone": "9999999999",
                    "country_code": "+91",
                    "password": "adminpass",
                    "role": "admin"
                },
                {
                    "first_name": "Store",
                    "last_name": "Manager",
                    "email": "store@email.com",
                    "phone": "8888888888",
                    "country_code": "+91",
                    "password": "storepass",
                    "role": "store"
                }
            ]
        }


class CustomerInDB(Customer):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
