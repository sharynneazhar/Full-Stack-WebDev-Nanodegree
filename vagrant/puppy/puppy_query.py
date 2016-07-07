from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Shelter, Puppy
import datetime
import decimal

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def query_all():
    puppies = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
    for puppy in puppies:
        # results return a tuple
        print puppy[0]

def query_younger_than_six_months():
    today = datetime.date.today()
    sixMonthsAgo = today - datetime.timedelta(days = 182)
    puppies = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

    for puppy in puppies:
        print "{name}: {dob}".format(name=puppy[0], dob=puppy[1])

def query_by_weight():
    puppies = session.query(Puppy.name, Puppy.weight)\
        .order_by(Puppy.weight.asc()).all()

    for puppy in puppies:
        weight = format(puppy[1], '.2f')
        print "{name}: {weight} lbs".format(name=puppy[0], weight=weight)

def query_by_shelter():
    puppies = session.query(func.count(Puppy.id), Shelter.name)\
        .join(Puppy.shelter)\
        .group_by(Shelter.id)\
        .all()

    for puppy in puppies:
        # results return a tuple
        print "{shelter}: {count}".format(count=puppy[0], shelter=puppy[1])

# query_all()
# query_younger_than_six_months()
# query_by_weight()
# query_by_shelter()
