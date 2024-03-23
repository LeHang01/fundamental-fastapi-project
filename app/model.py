import email
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from app.config import Base
from sqlalchemy.orm import relationship
import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone_number = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime)
    payments = relationship("Payment", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    orders = relationship("Order", back_populates="product")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    status = Column(String)
    payment_method = Column(String)

    user = relationship("Users", back_populates="payments")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.datetime.now())
    payment_status = Column(String, default="unpaid")

    user = relationship("Users", back_populates="orders")
    product = relationship("Product", back_populates="orders")