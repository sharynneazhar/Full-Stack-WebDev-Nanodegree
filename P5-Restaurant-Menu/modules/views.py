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
# RESTAURANT VIEWS
##############################################

# Main page
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = app.getRestaurants()
    if 'username' not in login_session:
        return render_template('restaurant_public.html',
                               restaurants=restaurants)
    else:
        user_id = login_session['user_id']
        return render_template('restaurant.html', restaurants=restaurants, user_id=user_id)


@app.route('/restaurants/search', methods=['GET', 'POST'])
def searchCategory():
    if request.method == 'POST':
        category = request.form['search']
        restaurants = app.getRestaurantsByCategory(category)

        if not restaurants:
            flash('Category not found.')
            return redirect(url_for('showRestaurants'))

        if 'username' not in login_session:
            return render_template('restaurant_public.html',
                                   restaurants=restaurants)

        return render_template('restaurant.html', restaurants=restaurants)


# Add new restaurant
@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login/')

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        user_id = login_session['user_id']
        restaurant = Restaurant(name=name, category=category, user_id=user_id)
        app.session.add(restaurant)
        app.session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('showRestaurants'))

    return render_template('newRestaurant.html')


# Edit restaurant info
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = app.getRestaurantsById(restaurant_id)

    if 'username' not in login_session:
        return redirect('/login/')

    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() " + \
        "{alert('You are not authorized to edit this restaurant. Please " + \
        "create your own restaurant in order to edit.');" + \
        "window.location.href='/';}</script>" + \
        "<body onload='myFunction()''>"

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        restaurant.name = name
        restaurant.category = category
        app.session.add(restaurant)
        app.session.commit()
        flash('Restaurant Successfully Edited!')
        return redirect(url_for('showRestaurants'))

    return render_template('editRestaurant.html', restaurant=restaurant)


# Delete restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = app.getRestaurantsById(restaurant_id)

    if 'username' not in login_session:
        return redirect('/login/')

    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() " + \
        "{alert('You are not authorized to delete this restaurant. Please " + \
        "create your own restaurant in order to delete.');" + \
        "window.location.href='/';}</script>" + \
        "<body onload='myFunction()''>"

    if request.method == 'POST':
        app.session.delete(restaurant)
        app.session.commit()
        flash('Restaurant Successfully Deleted!')
        return redirect(url_for('showRestaurants'))

    return render_template('deleteRestaurant.html', restaurant=restaurant)


##############################################
# MENU VIEWS
##############################################

# Show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    menu = app.getMenu(restaurant_id)
    restaurant = app.getRestaurantsById(restaurant_id)
    creator = app.getUserInfo(restaurant.user_id)

    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('menu_public.html',
                               restaurant=restaurant,
                               menu=menu,
                               creator=creator)
    else:
        return render_template('menu.html',
                               restaurant=restaurant,
                               menu=menu,
                               creator=creator)


# Add new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = app.getRestaurantsById(restaurant_id)

    if 'username' not in login_session:
        return redirect('/login/')

    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() " + \
        "{alert('You are not authorized to add to this restaurant. Please " + \
        "create your own restaurant in order to edit.');" + \
        "window.location.href='/';}</script>" + \
        "<body onload='myFunction()''>"

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        course = request.form['course']
        user_id = restaurant.user_id

        menuItem = MenuItem(name=name,
                            price=price,
                            description=description,
                            course=course,
                            restaurant_id=restaurant_id,
                            user_id=user_id)

        app.session.add(menuItem)
        app.session.commit()
        flash('Menu Item Created!')
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant=restaurant)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItem = app.getMenuItem(menu_id)
    restaurant = app.getRestaurantsById(restaurant_id)

    if 'username' not in login_session:
        return redirect('/login/')

    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() " + \
        "{alert('You are not authorized to edit this menu item. Please " + \
        "create your own menu item in order to edit.');" + \
        "window.location.href='/';}</script>" + \
        "<body onload='myFunction()''>"

    if request.method == 'POST':
        menuItem.name = request.form['name']
        menuItem.price = request.form['price']
        menuItem.description = request.form['description']
        menuItem.course = request.form['course']

        app.session.add(menuItem)
        app.session.commit()
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
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItem = app.getMenuItem(menu_id)
    restaurant = app.getRestaurantsById(restaurant_id)

    if 'username' not in login_session:
        return redirect('/login/')

    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() " + \
        "{alert('You are not authorized to delete this menu item. Please " + \
        "create your own menu item in order to delete.');" + \
        "window.location.href='/';}</script>" + \
        "<body onload='myFunction()''>"

    if request.method == 'POST':
        app.session.delete(menuItem)
        app.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteMenuItem.html',
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            menuItem=menuItem
        )
