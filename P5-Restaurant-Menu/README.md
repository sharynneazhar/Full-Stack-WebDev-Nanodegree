# Breadcrumbs
A project from Udacity's Full Stack Web Developer Nanodegree Program

#### Project Description
You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and an authentication system. Registered users will have the ability to post, edit and delete their own items.

#### Getting Started
###### What You Might Need
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* Clone the repo using `git clone https://github.com/sharynneazhar/fs-nanodegree.git`

###### Secret Keys
You need to obtain your own secret keys from [Google API](https://console.developers.google.com/) and [Facebook Developer](https://developers.facebook.com/). A guide to obtaining a Google client ID can be viewed [here](https://www.youtube.com/watch?v=8aGoty0VXgw). Once you register the app, you will be able to download the client secret JSON files required for the project. You may save the files under `/fs-nanodegree/P5-Restaurant-Menu/`. (Note: Udacity reviewers will be provided the necessary client IDs and secret keys under project submission notes)

###### Run the Project
* Run the virtual environment
  * `cd /path/to/fs-nanodegree` into the repo
  * `vagrant up && vagrant ssh` to the Vagrant VM
  * `cd /vagrant/P5-Restaurant-Menu` into the project directory
* Project Setup
  * `python models.py` to create the database
  * `python restaurantData.py` to fill in the database with mock data
  * `python app.py` to run the project
* Run The Project
  * Navigate to `localhost:5000` to see it working!

#### API Overview
* `/api/restaurants/` to obtain a list of all restaurants
* `/api/restaurants/<int:restaurant_id>/menu/` to obtain the menu list of a particular restaurant
* `/api/restaurants/<int:restaurant_id>/menu/<int:menu_id>` to obtain details about a particular menu item

#### Bugs / Future Improvements
* Feature: Integrate Yelp API to include more robust restaurant data
* Feature: Allow for multiple restaurant managers or roles (request access to edit/delete)
* Bug: Google+ authentication throws JSON serializable error randomly
