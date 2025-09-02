class Firm(Base):
    __tablename__ = "firms"
    id = Column(Integer, primary_key=True)
    cik = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    holdings = relationship("ThirteenFHolding", back_populates="firm")
