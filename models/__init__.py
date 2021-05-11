from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.number_plates_model import NumberPlates

con_url = 'postgresql://postgres:password@localhost:5432/anpr'

engine = create_engine(con_url, isolation_level='AUTOCOMMIT')

Session = sessionmaker(bind=engine)
session = Session()


def insert_number_plates_entry(vrn: str):
    entry = NumberPlates(vrn=vrn)
    session.add(entry)
    session.commit()


def search_number_plates_table(input_vrn: str):
    allowed_vrns = set()
    for vrn, in session.query(NumberPlates.vrn).all():
        allowed_vrns.add(vrn)

    if input_vrn in allowed_vrns:
        return True
    return False


def test_function():
    for row in session.query(NumberPlates, NumberPlates.vrn):
        print(row)
