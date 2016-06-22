from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def restaurants():
    results = session.query(Restaurant.name)\
        .order_by(Restaurant.name.asc())\
        .all()

    return results

def restaurants_by_id(id):
    results = session.query(Restaurant)\
        .filter_by(id)\
        .one()

    return results
