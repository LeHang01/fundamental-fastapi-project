from sqlalchemy.orm import Session
from app.models.Order_model import Order
from app.crud.order_crud import create_order
from app.schema.Order_schema import OrderCreateSchema
from typing import List, Optional

class OrderService:
    def __init__(self, order_crud: create_order) -> None:
        self.order_crud = order_crud

    async def get_order_by_id(self, session: Session, order_id: int) -> Optional[Order]:
        return await self.order_crud.get_by_id(session, id=order_id)

    async def get_all_orders(self, session: Session) -> List[Order]:
        return await self.order_crud.get_multi(session)

    async def create_order(self, session: Session, order: OrderCreateSchema) -> Order:
        return await self.order_crud.create(session, obj_in=order)

    async def delete_order(self, session: Session, order_id: int) -> Order:
        return await self.order_crud.remove(session, id=order_id)
