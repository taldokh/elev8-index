from sqlalchemy.orm import relationship

from models.base import Base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP, func

class IndexPoint(Base):
    __tablename__ = 'index_points'

    id = Column(Integer, primary_key=True)
    day_start_points = Column(Integer, nullable=False)
    day_end_points = Column(Integer, nullable=False)
    market_date = Column(Date, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    configuration_id = Column(Integer, ForeignKey("configurations.id", ondelete="CASCADE"), nullable=False)

    configuration = relationship("Configuration", back_populates="index_points")
