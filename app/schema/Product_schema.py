from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    title: str
    description: str
    price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int

class RequestProduct(BaseModel):
    pass