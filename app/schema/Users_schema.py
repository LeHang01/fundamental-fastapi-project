from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str
    first_name: str
    last_name: str


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None

class UserCreate(BaseModel):
    password: str

class UserUpdate(BaseModel):
    password: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str




class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]