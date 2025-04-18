from sqlalchemy import create_engine, Column, Integer, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from models.base import Base

class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    equities_per_firm = Column(Integer, nullable=False)
    number_of_firms = Column(Integer, nullable=False)
    selection_type_top = Column(Boolean, nullable=False)
    relative_weight = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('equities_per_firm', 'number_of_firms', 'selection_type_top', 'relative_weight'),
    )

    equities = relationship("Equity", back_populates="configuration", cascade="all, delete-orphan")
    index_points = relationship("IndexPoint", back_populates="configuration", cascade="all, delete-orphan")


