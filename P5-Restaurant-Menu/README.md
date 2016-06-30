# Breadcrumbs
A project from Udacity's Full Stack Web Developer Nanodegree Program

#### Project Description
You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and an authentication system. Registered users will have the ability to post, edit and delete their own items.

#### Running the App Locally
###### What You Need
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* Clone the repo using `git clone https://github.com/sharynneazhar/fs-nanodegree.git`

###### Run the Project
* `cd /path/to/fs-nanodegree` into the repo 
* `vagrant up && vagrant ssh` to the Vagrant VM
* `cd /vagrant/P5-Restaurant-Menu` into the project directory
* `python models.py` to create the database
* `python restaurantData.py` to fill in the database with mock data
* `python app.py` to run the project

Visit `localhost:5000` to see it working! 
