# Tournament Results
A project from Udacity's Full Stack Web Developer Nanodegree Program

#### Project Description
You will develop a database schema to store the game matches between players. You will then write a Python module to rank the players and pair them up in matches in a tournament. You will learn how to architect and develop a database containing fully normalized data within multiple tables. You’ll then learn how to modify this data and query it to meet the demands of a variety of use cases.

#### Running the Project
###### What You Need
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* Clone the repo using ```git clone https://github.com/sharynneazhar/fullstack-nanodegree-vm.git```

###### Run the Project
* Launch the Vagrant VM using ```vagrant up && vagrant ssh```
* ```cd``` into the ```vagrant/tournament``` directory
* Connect to the database server using the following command ```psql -f tournament.sql```
* Run the test suit using ```python tournament_test.py```
