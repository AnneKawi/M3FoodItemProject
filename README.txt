Food-Shopping-Website

a small website where we can catalog the items we buy for food and can register, how many we need to buy


- run python basicdata.py to populate the db
- run views.py to start the server
- runs on localhost:8000/
- basic overview is localhost:8000/catalog

APIs:
'/foodclass/foodclass_id_number/food.JSON' returns a json of all the food Items in this FoodClass
'/foodclass/foodclass_id_number/food/fooditem_id_number.JSON' returns a json of the chosen food_item
