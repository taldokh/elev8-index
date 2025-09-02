from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from models.base import Base

class ThirteenFHolding(Base):
    __tablename__ = "thirteenf_holdings"
    id = Column(Integer, primary_key=True)
    firm_id = Column(Integer, ForeignKey("firms.id", ondelete="CASCADE"))
    quarter = Column(String, nullable=False)  # e.g. "2023Q1"
    cusip = Column(String, nullable=False)
    ticker = Column(String, nullable=True)
    name_of_issuer = Column(String)
    value = Column(Float)
    ssh_prnamt = Column(Float)
    ssh_prnamt_type = Column(String)
    investment_discretion = Column(String)
    other_manager = Column(String, nullable=True)
    sole = Column(Integer)
    shared = Column(Integer)
    none = Column(Integer)

    firm = relationship("Firm", back_populates="holdings")

    __table_args__ = (UniqueConstraint("firm_id", "quarter", "cusip", name="uq_firm_quarter_cusip"),)