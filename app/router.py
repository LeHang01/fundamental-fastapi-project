from fastapi import APIRouter, Depends, HTTPException, Path

from app.crud.order_crud import create_order
from app.crud.payment_crud import PaymentRepo
from app.crud.users_crud import UsersRepo, JWTRepo, JWTBearer
from app.models.Users_model import Users
from app.schema.Order_schema import OrderCreateSchema
from app.schema.Users_schema import UserCreate, UserUpdate, RequestSchema, ResponseSchema, TokenResponse, Response
from app.schema.Product_schema import ProductCreate, ProductUpdate, ProductBase, RequestProduct
from sqlalchemy.orm import Session
from app.config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES, SessionLocal
from passlib.context import CryptContext

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
        existing_user = UsersRepo.find_by_username(db, Users, request.username)
        if existing_user:
            # Nếu đã có tài khoản với username này, trả về lỗi
            return ResponseSchema(
                code="400",
                status="Bad Request",
                message="Username already exists"
            ).dict(exclude_none=True)

        # Tạo và thêm tài khoản mới nếu username không trùng
        _user = Users(
            username=request.username,
            email=request.email,
            phone_number=request.phone_number,
            password=pwd_context.hash(request.password),
            first_name=request.first_name,
            last_name=request.last_name
        )
        UsersRepo.insert(db, _user)

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Success save data"
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500",
            status="Error",
            message="Internal Server Error"
        ).dict(exclude_none=True)


@auth_router.post('/login')
async def login(request: RequestSchema, db: Session = Depends(get_db)):
    try:
        # Lấy thông tin đăng nhập từ yêu cầu
        username = request.username
        password = request.password

        # Tìm người dùng dựa trên tên người dùng (username)
        _user = UsersRepo.find_by_username(db, Users, username)

        # Kiểm tra mật khẩu
        if not _user or not pwd_context.verify(password, _user.password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid username or password").dict(
                exclude_none=True)

        # Tạo và trả về mã thông báo (token)
        token = JWTRepo.generate_token({"sub": _user.username})
        return ResponseSchema(code="200", status="OK", message="Success login!",
                              result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error").dict(
            exclude_none=True)


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
    return Response(status="Ok", code="200", message="product created successfully", result={}).dict(exclude_none=True)


@pro_router.get("/")
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _products = crud.get_product(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_products)


@pro_router.patch("/update")
async def update_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(
        db,
        product_id=request.parameter.id,
        product=request.parameter
    )
    return Response(
        status="Ok",
        code="200",
        message="Success update data",
        result=_product
    ).dict(exclude_none=True)


@pro_router.delete("/delete")
async def delete_product(request: RequestProduct, db: Session = Depends(get_db)):
    crud.remove_product(db, product_id=request.parameter.id)
    return ResponseSchema(code="200", status="Ok", message="Success delete data", result={})


order_router = APIRouter()


@order_router.post("/orders/")
async def create_order_route(order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    try:
        order = create_order(db, user_id=order_data.user_id, product_id=order_data.product_id,
                             quantity=order_data.quantity)
        PaymentRepo.update_payment_status(db, order.id, "pending")
        return {"message": "Order created successfully", "order": order}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))