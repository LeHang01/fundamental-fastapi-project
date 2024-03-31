from typing import List, Optional

from requests import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users_crud import UsersCRUD
from app.models.Users_model import Users
from app.schema.Users_schema import UserCreate, UserUpdate

class UsersService:
    def __init__(self, user_crud: UsersCRUD) -> None:
        self.user_crud = user_crud

    async def get_user_by_id(self, session: Session, user_id: int) -> Optional[Users]:
        return await self.user_crud.get_by_id(session, id=user_id)

    async def get_all_users(self, session: Session) -> List[Users]:
        return await self.user_crud.get_multi(session)

    async def create_user(self, session: Session, user: UserCreate) -> Users:
        return await self.user_crud.create(session, obj_in=user)

    async def update_user(self, session: Session, user_id: int, user: UserUpdate) -> Users:
        return await self.user_crud.update(session, obj_in=user, id=user_id)

    async def delete_user(self, session: Session, user_id: int) -> Users:
        return await self.user_crud.remove(session, id=user_id)
