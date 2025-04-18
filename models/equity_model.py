from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from models.configuration_model import Configuration  # Adjust import path as needed
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base


class Equity(Base):
    __tablename__ = 'equities'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), nullable=False)
    quarter = Column(Date, nullable=False)
    weight = Column(Numeric(7, 4), nullable=False)
    configuration_id = Column(Integer, ForeignKey('configurations.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    configuration = relationship("Configuration", back_populates="equities")
