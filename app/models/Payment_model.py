import email
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, DateTime
from app.config import Base
from sqlalchemy.orm import relationship


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    status = Column(String)
    payment_method = Column(String)

    user = relationship("Users", back_populates="payments")
