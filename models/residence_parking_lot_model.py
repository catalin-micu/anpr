from sqlalchemy import Column, BigInteger, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ResidenceParkingLot(Base):
    __tablename__ = 'residence_parking_lot'

    id = Column(BigInteger, primary_key=True)
    vrn = Column(Text)
    event_date = Column(DateTime)
    event_type = Column(Text)
