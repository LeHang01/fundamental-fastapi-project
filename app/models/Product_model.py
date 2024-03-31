import email
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from app.config import Base
from sqlalchemy.orm import relationship
import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    orders = relationship("Order", back_populates="product")

