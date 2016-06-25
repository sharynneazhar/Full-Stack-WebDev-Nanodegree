from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify

from sqlalchemy import create_engine, func
from sqlalchemy.sql import collate
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

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
        return redirect(url_for('showRestaurants'))
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
        return redirect(url_for('showRestaurants'))
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
