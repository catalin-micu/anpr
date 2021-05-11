from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class NumberPlates(Base):
    __tablename__ = 'number_plates'

    id = Column(BigInteger, primary_key=True)
    vrn = Column(Text)
