from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text, TIMESTAMP, BigInteger, func, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from models.base import Base

class ThirteenFHolding(Base):
    __tablename__ = 'thirteenf_holdings'

    id = Column(Integer, primary_key=True)
    firm_id = Column(Integer, ForeignKey('firms.id', ondelete='CASCADE'))
    ticker = Column(String, nullable=False)
    cusip = Column(String, nullable=False)
    name_of_issuer = Column(String)
    value = Column(BigInteger)
    shares = Column(BigInteger)
    put_call = Column(String)
    discretion = Column(String)
    quarter = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    firm = relationship("Firm", back_populates="thirteenf_holdings")