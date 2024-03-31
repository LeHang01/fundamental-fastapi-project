from app.crud.base_crud import CRUDBase
from app.models.Product_model import Product
from app.schema.Product_schema import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product_crud = CRUDProduct(Product)
