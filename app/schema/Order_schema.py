from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None



class OrderCreateSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int

