from typing import List, Optional

from app.crud.product_crud import product_crud
from app.models.Product_model import Product
from app.schema.Product_schema import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class ProductService:
    async def get_products(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
        return await product_crud.get_multi(db, skip=skip, limit=limit)

    async def create_product(self, db: AsyncSession, product: ProductCreate) -> Product:
        return await product_crud.create(db, obj_in=product)

    async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Optional[Product]:
        return await product_crud.get(db, product_id)

    async def update_product(self, db: AsyncSession, product_id: int, product: ProductUpdate) -> Product:
        return await product_crud.update(db, product_id=product_id, obj_in=product)

    async def delete_product(self, db: AsyncSession, product_id: int) -> Product:
        return await product_crud.delete(db, product_id=product_id)
