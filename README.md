# FAVORITE THINGS TRACKER


A "Favorite Things Tracker" is a system that allows users to track or take note of things which include people, places, foods, events, etc with the use of a Vue SPA (Single Page Application) consuming a Django REST framework.
 


## Approach to Problem Statement
* Three different database tables were used to implement this, the Profile (in a onetoone relationship with the default Django User table), the Category and the List tables.

* The Profile table is used to manage users' details such as id, username, email address, and password (password was added because any user's favorite list has to be confidential, protected and only made available to that particular user). 

* The Category table is used manage the default categories (Places, People  and Food) and also to manage the categories that will be created by other users (kindly note that any new category created by a user is visible and only made available to the user and only this user can make use of it). The columns present in the Category table include (id, name, user_id). 

* The List table helps to manage the list of favorite things by all users, it has the following columns (id, rid, title, description, ranking, user_id, cat, created_date, modified_date and log).

##Scope

When a new favorite list is to be added by a particular user, the following conditions are satisfied:

* User must be logged in

* The description length must be greater than 1 character.

* The user can select from the following list of categories People, Place, Food and all  other categories created by this user.

* When a ranking value is submitted, the system checks through the List table for the favorite things added by this particular user with the same category submitted, if any of the favorite things checked for has the same ranking value with the newly submitted favorite thing, the ranking number of the existing favorite thing changes to the sum of the highest ranking in that category for the particular user and one. Thus, the newly submitted favorite thing maintains its own ranking value.


##Features of the solution
*  A REST API built with Django REST framework with three class based API_VIEWS (listed in the API endpoint section) which can handle GET, POST and PUT requests.
* User login implemented with Django authenticate()
* Django ORM used for querying the database
* PostgreSQL database
* Bootstrap framework used for the UI
* Vue-CLI Javascript framework used for the frontend

## How to get Started

The instructions bellow will get this project up and running on your PC (type in all commands in your command line, having navigated to th project directory on your PC)

* Step 1 

Install packages

```
$ pip install -r requirements.txt
```
* Step 2

Initialize Virtual Environment
```
$ source venv/bin/activate
```
* Step 3

`from the root directory from the project run the following command`

```
python manage.py runserver
```


* Step 4

You can now start interacting with the web app

`URL: ` <http://127.0.0.1:8000> 

#### API ENDPOINTS ON LOCALHOST
`Profile: ` <http://127.0.0.1:8000/api/profile> You can `GET` , `POST` and `PUT` 

`Category: ` <http://127.0.0.1:8000/api/category> You can `GET` , `POST` and `PUT` 

`List: ` <http://127.0.0.1:8000/api/list> You can `GET` , `POST` and `PUT` 



## Live Version

`To setup on a live server follow this link:`
* [SETUP Docker Container](https://docs.docker.com/compose/django/) - deployment of the Django app with Docker
* [Deploying a Vue App inside a Django App](https://medium.com/@williamgnlee/simple-integrated-django-vue-js-web-application-configured-for-heroku-deployment-c4bd2b37aa70) - deploying the Vue app after running `npm run build` to get the production ready Vue app
* Then setup HTTP(S) load balancing to serve over port 443

`For live testing, visit`
<https://www.spibes.com/>

#### API ENDPOINTS ONLINE
`ProfileEndpoints: ` <https://www.spibes.com/api/profile> You can `GET` , `POST` and `PUT` 

`CategoryEndpoints: ` <https://www.spibes.com/api/cat> You can `GET` , `POST` and `PUT` 

`ListEndpoints: ` <https://www.spibes.com/api/list> You can `GET` , `POST` and `PUT` 

#### POSSIBLE QUERIES FOR THE ONLINE VERSION OF THE API
* Create a new user using POST to Profile endpoint, payload `[username, email, fname, lname, password1, password2]`
* Login a user using get parameter passing username=username and password=password as GET arguments
* Update user's details using PUT to Profile endpoint, payload `[username, email, fname, lname, password1, password2]`
* Query all profiles by using GET without passing any argument
* Query the categories owned by a user by passing who=email as a GET argument
* Query all categories by using GET to Category endpoint without passing any argument
* Create a new category by using POST to the endpoint, payload `[email, name]`
* Query all favorite list by using GET to the List endpoint without passing any argument
* Query all favorite list by passing a cat=cat_id GET argument to the list endpoint
* Query all favorite list owned by a particular user by passing a who=email GET argument to the endpoint
* Query all favorite list owned by a user and under a specified category using who=email and cat=cat_id GET arguments to the endpoint
* Create a new favorite list with POST to the endpoint, payload `[email, title, description, cat, ranking]`
* Update a favorite list with PUT to the endpoint, payload `[id, email, title, description, cat, ranking]`


## Built With

* [Django](http://www.djangoproject.com/) - Python web framework used for REST API
* [GCP (Compute Engine)](https://console.cloud.google.com/) - Hosting Platform
* [VueJS](https://vuejs.org/) - Javascript framework used for frontend
* [Docker](https://docs.docker.com/compose/django/) - Server side container


