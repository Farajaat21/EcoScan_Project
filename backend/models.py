from sqlalchemy import Column, Integer, String, JSON
try:
	from .database import Base
except ImportError:
	from database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, index=True)
    score = Column(Integer)
    breakdown = Column(JSON)
