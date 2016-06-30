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
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = app.getRestaurants()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    menu = app.getMenu(restaurant_id)
    return jsonify(Menu=[i.serialize for i in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = app.getMenuItem(menu_id)
    return jsonify(MenuItem=menuItem.serialize)
