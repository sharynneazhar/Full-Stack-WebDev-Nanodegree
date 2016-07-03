from flask import Flask
from flask import session as login_session

from sqlalchemy import create_engine, func
from sqlalchemy.sql import collate
from sqlalchemy.orm import sessionmaker

from models import Base, User, Restaurant, MenuItem

app = Flask(__name__)

import modules.views
import modules.api
import modules.signin

engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app.session = session

###############################################
# HELPER FUNCTIONS
##############################################
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    return session.query(User)\
        .filter_by(email=login_session['email'])\
        .first()
app.createUser = createUser


def getUserInfo(user_id):
    return session.query(User)\
        .filter_by(id=user_id)\
        .first()
app.getUserInfo = getUserInfo


def getUserID(email):
    try:
        user = session.query(User)\
            .filter_by(email=email)\
            .one()
        return user.id
    except:
        return None
app.getUserID = getUserID


def getRestaurants():
    return session.query(Restaurant)\
        .order_by(collate(Restaurant.name, 'NOCASE'))\
        .all()
app.getRestaurants = getRestaurants


def getRestaurantsById(restaurant_id):
    return session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .first()
app.getRestaurantsById = getRestaurantsById


def getRestaurantsByCategory(category):
    return session.query(Restaurant)\
        .filter(func.lower(Restaurant.category) == func.lower(category))\
        .all()
app.getRestaurantsByCategory = getRestaurantsByCategory


def getMenu(restaurant_id):
    return session.query(MenuItem)\
        .filter_by(restaurant_id=restaurant_id)\
        .order_by(collate(MenuItem.name, 'NOCASE'))\
        .all()
app.getMenu = getMenu


def getMenuItem(menu_id):
    return session.query(MenuItem)\
        .filter_by(id=menu_id)\
        .first()
app.getMenuItem = getMenuItem
