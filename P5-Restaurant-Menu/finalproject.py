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

# Main pagee
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant)\
        .order_by(collate(Restaurant.name, 'NOCASE'))\
        .all()

    return render_template('restaurant.html', restaurants=restaurants)

# Add new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form['name']
        restaurant = Restaurant(name=name)
        session.add(restaurant)
        session.commit()
        flash('Added %s!' % name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# Edit restaurant info
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()

    if request.method == 'POST':
        name = request.form['name']
        restaurant.name = name
        session.add(restaurant)
        session.commit()
        flash('Successfully renamed restaurant to %s' % name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)

# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()

    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Removed %s from list!' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)

# Show a resturant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    menu = session.query(MenuItem)\
        .filter_by(restaurant_id=restaurant_id)\
        .order_by(collate(MenuItem.name, 'NOCASE'))\
        .all()

    restaurant = session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()

    return render_template('menu.html', restaurant=restaurant, menu=menu)

# Add new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant)\
        .filter_by(id=restaurant_id)\
        .one()

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
        flash('Added %s!' % name)
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    return render_template(
        'editMenuItem.html',
        restaurant_id=restaurant_id,
        menu_id=menu_id,
    )

# Delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem)\
        .filter_by(id=menu_id)\
        .one()

    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('Removed %s from list!' % menuItem.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template(
            'deleteMenuItem.html',
            restaurant_id=restaurant_id,
            menu_id=menu_id,
        )


if __name__ == '__main__':
    app.secret_key = 'qtXgBxqhrN'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
