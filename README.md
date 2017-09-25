# Food-Shopping-Website

A small website where we can catalog the items we buy for food and can register, how many we need to buy. Though in order to make any change in the data, you need to log in with your Google-account.

## prerequisites
you will need:
- python2.7 or newer with the modules
    - sqlalchemy
    - flask
    - oauth2client
- sqlite
installed on your machine

## get the website up and running
- clone the repository to your machine
- run **python database_setup.py** to initialize the database
- run **python basicdata.py** to populate the db
- run **python views.py** to start the server
- runs in your favorite Webbrowser on **http://localhost:8000/**
- you will find the basic overview on **http://localhost:8000/catalog**

## how to use the APIs:
- '/foodclasses/JSON' returns a json with all available foodclasses and their ids
- '/foodclass/foodclass_id_number/food/JSON' returns a json of all the food Items in this FoodClass
- '/foodclass/foodclass_id_number/food/fooditem_id_number/JSON' returns a json of the chosen food_item


## References:
- the authentication routine was taken from the oauth-class and only adapted to the needs of the project
