import os
import random
import string
import httplib2
import json
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from flask import session as login_session
from flask import make_response

from sqlalchemy import create_engine, func
from sqlalchemy.sql import collate
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from modules import app
from models import Base, User, Restaurant, MenuItem


##############################################
# JSON RESPONSE API
##############################################
@app.route('/api/restaurants/')
def restaurantJSON():
    """
    Returns the JSON data for the list of restaurants
    """
    restaurants = app.getRestaurants()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/api/restaurants/<int:restaurant_id>/menu/')
def menuJSON(restaurant_id):
    """
    Returns the JSON data for the list of
    menu items at a  particular restaurant
    """
    menu = app.getMenu(restaurant_id)
    return jsonify(Menu=[i.serialize for i in menu])


@app.route('/api/restaurants/<int:restaurant_id>/menu/<int:menu_id>/')
def menuItemJSON(restaurant_id, menu_id):
    """
    Returns the JSON data for the menu item details
    """
    menuItem = app.getMenuItem(menu_id)
    return jsonify(MenuItem=menuItem.serialize)
