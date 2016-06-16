# [redr](http://redr-0613.appspot.com/)
A project from Udacity's Full Stack Web Developer Nanodegree Program

#### Project Description
In this project you will be building a multi user blog(along the lines of Medium) where users can sign in and post blog posts as well as 'Like' and 'Comment' on other posts made on the blog. You will be hosting this blog on Google App Engine (GAE) and you will also be creating an authentication system for users to be able to register and sign in and then create blog posts!

#### Running the Project Locally
###### Pre-requisites
* Install the GAE for Python SDK [here](https://cloud.google.com/appengine/downloads)
* Sign up for a GAE account ([instructions](https://sites.google.com/site/gdevelopercodelabs/app-engine/creating-your-app-engine-account))
* Clone the repo with ```git clone https://github.com/sharynneazhar/full-stack-webdev-nanodegree.git```
* ```cd P3-Blog``` into the blog directory

You may run the project several ways:
1. You can use the GAE to run the app. Simply start the launcher, add the app as an existing project, hit run, and you can view the blog site through your localhost
2. If you are on a Windows OS:
  * Run ``` .\rundev.bat \path\to\P3-Blog ```
  * Note: This assumes that your GAE is installed under Program Files (x86)
3. If you are on a Mac OS:
  * Run ``` dev_appserver.py \path\to\P3-Blog ```
  * Note: This assumes that you have created a symlink during the GAE installation
