from fastapi import APIRouter, Depends, HTTPException, Path
from app.schema import RequestSchema, ResponseSchema, TokenResponse, ProductSchema, Request, Response, RequestProduct, OrderCreateSchema
from sqlalchemy.orm import Session
from app.config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES, SessionLocal
from passlib.context import CryptContext
from app.repository import JWTRepo, JWTBearer, UsersRepo
from app.model import Users
from app.order import create_order
from datetime import datetime, timedelta
from app import crud

auth_router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
    Authentication Router

"""


@auth_router.post('/signup')
async def signup(request: RequestSchema, db: Session = Depends(get_db)):
    try:
        # insert user to db
        _user = Users(username=request.parameter.data["username"],
                      email=request.parameter.data["email"],
                      phone_number=request.parameter.data["phone_number"],
                      password=pwd_context.hash(
                          request.parameter.data["password"]),
                      first_name=request.parameter.data['first_name'],
                      last_name=request.parameter.data['last_name'])
        UsersRepo.insert(db, _user)
        return ResponseSchema(code="200", status="Ok", message="Success save data").dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error").dict(exclude_none=True)


@auth_router.post('/login')
async def login(request: RequestSchema, db: Session = Depends(get_db)):
    try:
       # find user by username
        _user = UsersRepo.find_by_username(
            db, Users, request.parameter.data["username"])

        if not pwd_context.verify(request.parameter.data["password"], _user.password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid password").dict(exclude_none=True)

        token = JWTRepo.generate_token({"sub": _user.username})
        return ResponseSchema(code="200", status="OK", message="success login!", result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error").dict(exclude_none=True)


"""
    Users Router

"""


@auth_router.get("/users", dependencies=[Depends(JWTBearer())])
async def retrieve_all(db: Session = Depends(get_db)):
    _user = UsersRepo.retrieve_all(db, Users)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_user).dict(exclude_none=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pro_router = APIRouter()
@pro_router.post("/create")
async def create_product_service(request: RequestProduct, db: Session = Depends(get_db)):
    crud.create_product(db, product=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="product created successfully").dict(exclude_none=True)


@pro_router.get("/")
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _products = crud.get_product(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_products)


@pro_router.patch("/update")
async def update_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(db, product_id=request.parameter.id,
                                   name=request.parameter.name,
                             title=request.parameter.title, description=request.parameter.description, price=request.parameter.price,
                             stock_quantity=request.parameter.stock_quantity)
    return Response(status="Ok", code="200", message="Success update data", result=_product)


@pro_router.delete("/delete")
async def delete_product(request: RequestProduct,  db: Session = Depends(get_db)):
    crud.remove_product(db, product_id=request.parameter.id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)


order_router = APIRouter()

@order_router.post("/orders/")
async def create_order_route(order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    try:
        order = create_order(db, user_id=order_data.user_id, product_id=order_data.product_id, quantity=order_data.quantity)
        return {"message": "Order created successfully", "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))