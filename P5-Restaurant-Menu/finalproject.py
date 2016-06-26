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

from db_setup import Base, Restaurant, MenuItem

import random
import string
import httplib2
import json
import requests


app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Breadcrumbs"

engine = create_engine('sqlite:///restaurant-data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#########################################
##          GLOBAL FUNCTIONS           ##
#########################################

def getRestaurants():
    return session.query(Restaurant)\
        .order_by(collate(Restaurant.name, 'NOCASE'))\
        .all()

def getRestaurantsById(restaurant_id):
    return session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()

def getMenu(restaurant_id):
    return session.query(MenuItem)\
        .filter_by(restaurant_id=restaurant_id)\
        .order_by(collate(MenuItem.name, 'NOCASE'))\
        .all()

def getMenuItem(menu_id):
    return session.query(MenuItem)\
        .filter_by(id=menu_id)\
        .one()


#########################################
##           API ENDPOINTS             ##
#########################################

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output

# Return all restaurant
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = getRestaurants()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

# Return menu for particular restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    menu = getMenu(restaurant_id)
    return jsonify(Menu=[i.serialize for i in menu])

# Return menu item for particular menu
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = getMenuItem(menu_id)
    return jsonify(MenuItem=menuItem.serialize)


#########################################
##       CLIENT-SIDE SERVICES          ##
#########################################

# Main pagee
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = getRestaurants()
    return render_template('restaurant.html', restaurants=restaurants)

# Add new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form['name']
        restaurant = Restaurant(name=name)
        session.add(restaurant)
        session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# Edit restaurant info
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = getRestaurantsById(restaurant_id)
    if request.method == 'POST':
        name = request.form['name']
        restaurant.name = name
        session.add(restaurant)
        session.commit()
        flash('Restaurant Successfully Edited!')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)

# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = getRestaurantsById(restaurant_id)
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant Successfully Deleted!')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)

# Show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    menu = getMenu(restaurant_id)
    restaurant = getRestaurantsById(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, menu=menu)

# Add new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = getRestaurantsById(restaurant_id)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        course = request.form['course']

        menuItem = MenuItem(name=name,
                            price=price,
                            description=description,
                            course=course,
                            restaurant_id=restaurant_id)

        session.add(menuItem)
        session.commit()
        flash('Menu Item Created!')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant=restaurant)

# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItem = getMenuItem(menu_id)
    if request.method == 'POST':
        menuItem.name = request.form['name']
        menuItem.price = request.form['price']
        menuItem.description = request.form['description']
        menuItem.course = request.form['course']

        session.add(menuItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editMenuItem.html',
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            menuItem=menuItem
        )

# Delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = getMenuItem(menu_id)
    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteMenuItem.html',
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            menuItem=menuItem
        )


if __name__ == '__main__':
    app.secret_key = 'qtXgBxqhrN'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
