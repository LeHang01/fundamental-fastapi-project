import email
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from app.config import Base
from sqlalchemy.orm import relationship
import datetime

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