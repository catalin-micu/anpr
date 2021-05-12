from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.number_plates_model import NumberPlates
from models.residence_parking_lot_model import ResidenceParkingLot

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


def insert_residence_parking_lot_entry_duo(vrn: str, event_date: str, stay_duration: int, duration_type: str):
    """
    event_date format eg: datetime.now().isoformat()
    duration_type possibilities (literally): 'minutes', 'hours', 'days'
    """
    entry = ResidenceParkingLot(vrn=vrn, event_date=event_date, event_type='in')
    session.add(entry)

    exit_date = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S.%f')
    if duration_type == 'minutes':
        exit_date = exit_date + timedelta(minutes=stay_duration)
    elif duration_type == 'hours':
        exit_date = exit_date + timedelta(hours=stay_duration)
    elif duration_type == 'days':
        exit_date = exit_date + timedelta(days=stay_duration)

    entry = ResidenceParkingLot(vrn=vrn, event_date=exit_date, event_type='out')
    session.add(entry)

    session.commit()


def test_function():
    for row in session.query(NumberPlates, NumberPlates.vrn):
        print(row)
