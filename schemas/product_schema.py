from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    name: str = Field(...,example="Iphone 14")
    price: float = Field(..., gt=0, example=799.99)
    in_stock: Optional[bool] = Field(default=True, example=True)


class UpdateProductSchema(BaseModel):
    name:Optional[str] = Field(None,example="Iphone 13")
    price:Optional[float] = Field(None,gt = 0, example=999.99)
    in_stock:Optional[bool] = Field(None, example=False)