from datetime import datetime

from sqlalchemy import Column, DateTime, Text, TIMESTAMP, Integer, String, func, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from models.base import Base

class Firm(Base):
    __tablename__ = 'firms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cik = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    thirteenf_holdings = relationship("ThirteenFHolding", back_populates="firm", cascade="all, delete-orphan")
