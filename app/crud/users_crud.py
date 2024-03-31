from app.crud.base_crud import CRUDBase
from app.models.Users_model import Users
from app.schema.Users_schema import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class UsersCRUD(CRUDBase[Users, UserCreate, UserUpdate]):
    pass


class BaseRepo(Generic[T]):

    @staticmethod
    def retrieve_all(db: Session, model: T):
        return db.query(model).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: T, id: int):
        return db.query(model).filter(model.id == id).first()

    @staticmethod
    def insert(db: Session, model: T):
        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: T):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: T):
        db.delete(model)
        db.commit()


class UsersRepo(BaseRepo[Users]):

    @staticmethod
    def find_by_username(db: Session, model: Users, username: str):
        return db.query(model).filter(model.username == username).first()


class JWTRepo():

    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
            return decode_token if decode_token["exp"] >= datetime.utcnow() else None
        except JWTError:
            return None


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not JWTRepo().verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")
