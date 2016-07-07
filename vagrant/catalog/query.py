from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.sql import collate
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def restaurants():
    return session.query(Restaurant)\
        .order_by(collate(Restaurant.name, 'NOCASE'))\
        .all()

def restaurants_by_id(restaurant_id):
    return session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()
