from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import FoodClass, Base, FoodItem

engine = create_engine('sqlite:///foodlist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Build a User
user1 = User(username = 'Anne', email = 'annewirsig@yahoo.com')
user1.hash_password('apassword')
session.add(user1)
session.commit()

#Items for grains
foodclass1 = FoodClass(name = "Grains & grain products")

session.add(foodclass1)
session.commit()

for [name, description, price, typical_size] in [["Wheat Flour T550", "Wheat flour of the type 550", "2.55 €", '1 kg'],
                                                 ["Rye Flour T1150", "Rye flour of the type 1150, used for bread", "2.95 €", '1 kg'],
                                                 ["Rice", "polished rice", '1.99 €', '250 g'],
                                                 ['Popcorn-Mais', 'dried grains of popcorn mais', '3.50 €', '250 g'],
                                                 ['Spirelli', 'Spirelli noodles Nr. 32', '1.50 €', '250 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass1, creator = user1)

    session.add(foodItem1)
    session.commit()

#Items for milk products
foodclass2 = FoodClass(name = "Milk products")

session.add(foodclass2)
session.commit()

for [name, description, price, typical_size] in [["H-Milk", "H-Milk with 3,5% fat", "1.95 €", '1 litre'],
                                                 ["Cream", "Sweet Cream with > 30% fat", "2.95 €", '250 ml'],
                                                 ["Joghurt", "natural joghurt with 3,5% fat", '0.39 €', '125 ml'],
                                                 ['Parmesan', 'Dry well aged cheese from Parma region', '2.50 €', '100 g'],
                                                 ['Gorgonzola', 'blue cheese from some caves in France...', '2.80 €', '100 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass2, creator = user1)

    session.add(foodItem1)
    session.commit()


#Items for Fruit
foodclass3 = FoodClass(name = "Fruit")

session.add(foodclass3)
session.commit()

for [name, description, price, typical_size] in [["Apples", "whatever is in season and tastes well", "3.99 €", '1 kg'],
                                                 ["Banana", "only when sufficiently yellow", "1.95 €", '1 kg'],
                                                 ["Kiwi", "every now and then", '0.35 €', 'per piece'],
                                                 ['Grapes', 'when in season and edible', '3.50 €', '500 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass3, creator = user1)

    session.add(foodItem1)
    session.commit()

#Items for Vegetables
foodclass4 = FoodClass(name = "Vegetables")

session.add(foodclass4)
session.commit()

for [name, description, price, typical_size] in [["Onions white", "white onions", "3.55 €", '1 kg'],
                                                 ["Tomatos", "preferably roman tomatoes", "4.95 €", '1 kg'],
                                                 ["Potatoes", "Rosara is a nice type", '3.99 €', '1 kg'],
                                                 ['Broccoli', "take care they aren't yellow yet", '1.50 €', '250 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass4, creator = user1)

    session.add(foodItem1)
    session.commit()


#Items for Meat
foodclass5 = FoodClass(name = "Meat")

session.add(foodclass5)
session.commit()

for [name, description, price, typical_size] in [["Filet de boef", "filet steak from happy cows", "12.55 €", '500 g'],
                                                 ["pork belly", "fresh material from the 'Schweinchen'", "5.99 €", '250 g'],
                                                 ["pork belly ham", "ham from southern tirol", '1.99 €', '200 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass5, creator = user1)

    session.add(foodItem1)
    session.commit()


#Items for Sweets
foodclass6 = FoodClass(name = "Sweets")

session.add(foodclass6)
session.commit()

for [name, description, price, typical_size] in [["Jelly Fruit", "The best we have found yet and very fruity", "3.99 €", '200 g'],
                                                 ["American Cookies", "preferably the chocolate type, but ginger is fine too", "2.95 €", '250 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass6, creator = user1)

    session.add(foodItem1)
    session.commit()


#Items for Sugar, Salt & other
foodclass7 = FoodClass(name = "Sugar, Salt & Other")

session.add(foodclass7)
session.commit()

for [name, description, price, typical_size] in [["Light Sugar", "light coloured Cane sugar", "1.55 €", '1 kg'],
                                                 ["Brown Sugar", "unrefined brown cane sugar", "4.95 €", '1 kg'],
                                                 ["Salt with algae", "fine sea salt with algae", '1.50 €', '200 g'],
                                                 ['Raw sea salt', 'Sea salt with larger grains', '1.99 €', '500 g']]

    foodItem1 = FoodItem(name = name, description = description, price = price, typical_size = typical_size, need_to_shop = 0, foodclass = foodclass7, creator = user1)

    session.add(foodItem1)
    session.commit()


print "added food items!"
