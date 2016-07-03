import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Restaurant, Base, MenuItem, User
from modules import app


##############################################
# DUMMY USERS
##############################################
user1 = User(name="Robert Rista",
             email="robertrista@udacity.com",
             picture='https://cdn-selfish-prod.turbobytes.net/staged/host-prod/0912d4d717886001-0912d4d717886002.jpg')
app.session.add(user1)
app.session.commit()

user2 = User(name="Kelly Donahue",
             email="kdonahue@gmail.com",
             picture='http://www.hairstylestars.com/wp-content/uploads/2013/05/Hipster-Bangs.jpg')
app.session.add(user2)
app.session.commit()

user3 = User(name="Naomi Li",
             email="naomi.li@gmail.com",
             picture='http://www.huffingtonpost.com/contributors/sahra-vang-nguyen/headshot.jpg')
app.session.add(user3)
app.session.commit()


##############################################
# DUMMY RESTAURANTS
##############################################

# Menu for Urban Burger
restaurant1 = Restaurant(user_id=1, name="Urban Burger", category="American")
app.session.add(restaurant1)
app.session.commit()

menuItem1 = MenuItem(user_id=1,
                     name="French Fries",
                     description="With garlic and parmesan",
                     price="2.99",
                     course="Appetizer",
                     restaurant=restaurant1)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=1,
                     name="Veggie Burger",
                     description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="7.50",
                     course="Entree",
                     restaurant=restaurant1)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=2,
                     name="Chocolate Cake",
                     description="Fresh baked and served with ice cream",
                     price="3.99",
                     course="Dessert",
                     restaurant=restaurant1)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=1,
                     name="Sirloin Burger",
                     description="Made with grade A beef",
                     price="7.99",
                     course="Entree",
                     restaurant=restaurant1)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=1,
                     name="Root Beer",
                     description="16oz of refreshing goodness",
                     price="1.99",
                     course="Beverage",
                     restaurant=restaurant1)
app.session.add(menuItem5)
app.session.commit()

menuItem6 = MenuItem(user_id=2,
                     name="Iced Tea",
                     description="With Lemon",
                     price=".99",
                     course="Beverage",
                     restaurant=restaurant1)
app.session.add(menuItem6)
app.session.commit()

menuItem7 = MenuItem(user_id=1,
                     name="Grilled Cheese Sandwich",
                     description="On texas toast with American Cheese",
                     price="3.49",
                     course="Entree",
                     restaurant=restaurant1)
app.session.add(menuItem7)
app.session.commit()

menuItem8 = MenuItem(user_id=1,
                     name="Veggie Burger",
                     description="Made with freshest of ingredients and home grown spices",
                     price="5.99",
                     course="Entree",
                     restaurant=restaurant1)
app.session.add(menuItem8)
app.session.commit()


# Menu for Super Stir Fry
restaurant2 = Restaurant(user_id=2, name="Super Stir Fry", category="Asian")
app.session.add(restaurant2)
app.session.commit()

menuItem1 = MenuItem(user_id=2,
                     name="Chicken Stir Fry",
                     description="With your choice of noodles vegetables and sauces",
                     price="7.99",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=2,
                     name="Peking Duck",
                     description="A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook",
                     price="25",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=2,
                     name="Spicy Tuna Roll",
                     description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     price="15",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=3,
                     name="Nepali Momo",
                     description="Steamed dumplings made with vegetables, spices and meat.",
                     price="12",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=3,
                     name="Beef Noodle Soup",
                     description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     price="14",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem5)
app.session.commit()

menuItem6 = MenuItem(user_id=1,
                     name="Ramen",
                     description="A Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
                     price="12",
                     course="Entree",
                     restaurant=restaurant2)
app.session.add(menuItem6)
app.session.commit()


# Menu for Panda Garden
restaurant3 = Restaurant(user_id=3, name="Panda Garden", category="Asian")
app.session.add(restaurant3)
app.session.commit()

menuItem1 = MenuItem(user_id=3,
                     name="Pho",
                     description="A Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     price="8.99",
                     course="Entree",
                     restaurant=restaurant3)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=3,
                     name="Chinese Dumplings",
                     description="A common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     price="6.99",
                     course="Appetizer",
                     restaurant=restaurant3)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=1,
                     name="Gyoza",
                     description="Light seasoning of Japanese gyoza with salt and soy sauce, and in a thin gyoza wrapper",
                     price="9.95",
                     course="Entree",
                     restaurant=restaurant3)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=3,
                     name="Stinky Tofu",
                     description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     price="6.99",
                     course="Entree",
                     restaurant=restaurant3)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=2,
                     name="Veggie Burger",
                     description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$9.50",
                     course="Entree",
                     restaurant=restaurant3)
app.session.add(menuItem5)
app.session.commit()


# Menu for Thyme For That
restaurant4 = Restaurant(user_id=2, name="Thyme for That Vegetarian Cuisine", category="Vegetarian")
app.session.add(restaurant4)
app.session.commit()

menuItem1 = MenuItem(user_id=2,
                     name="Tres Leches Cake",
                     description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
                     price="$2.99",
                     course="Dessert",
                     restaurant=restaurant4)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=2,
                     name="Mushroom risotto",
                     description="Portabello mushrooms in a creamy risotto",
                     price="$5.99",
                     course="Entree",
                     restaurant=restaurant4)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=2,
                     name="Honey Boba Shaved Snow",
                     description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi",
                     price="$4.50",
                     course="Dessert",
                     restaurant=restaurant4)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=2,
                     name="Cauliflower Manchurian",
                     description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
                     price="$6.95",
                     course="Appetizer",
                     restaurant=restaurant4)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=2,
                     name="Aloo Gobi Burrito",
                     description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
                     price="$7.95",
                     course="Entree",
                     restaurant=restaurant4)
app.session.add(menuItem5)
app.session.commit()

menuItem6 = MenuItem(user_id=2,
                     name="Veggie Burger",
                     description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="6.80",
                     course="Entree",
                     restaurant=restaurant4)
app.session.add(menuItem6)
app.session.commit()


# Menu for Tony's Bistro
restaurant6 = Restaurant(user_id=1, name="Tony\'s Bistro", category="American")
app.session.add(restaurant6)
app.session.commit()

menuItem1 = MenuItem(user_id=1,
                     name="Shellfish Tower",
                     description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
                     price="13.95",
                     course="Entree",
                     restaurant=restaurant6)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=1,
                     name="Chicken and Rice",
                     description="Chicken... and rice",
                     price="4.95",
                     course="Entree",
                     restaurant=restaurant6)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=1,
                     name="Mom's Spaghetti",
                     description="Spaghetti with some incredible tomato sauce made by mom",
                     price="6.95",
                     course="Entree",
                     restaurant=restaurant6)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=1,
                     name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
                     description="Milk, cream, salt, ..., Liquid nitrogen magic",
                     price="3.95",
                     course="Dessert",
                     restaurant=restaurant6)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=1,
                     name="Tonkatsu Ramen",
                     description="Noodles in a delicious pork-based broth with a soft-boiled egg",
                     price="7.95",
                     course="Entree",
                     restaurant=restaurant6)
app.session.add(menuItem5)
app.session.commit()


# Menu for Andala's
restaurant7 = Restaurant(user_id=2, name="Andala\'s", category="Asian")
app.session.add(restaurant7)
app.session.commit()

menuItem1 = MenuItem(user_id=1,
                     name="Lamb Curry",
                     description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
                     price="9.95",
                     course="Entree",
                     restaurant=restaurant7)
app.session.add(menuItem1)
app.session.commit()

menuItem2 = MenuItem(user_id=2,
                     name="Chicken Marsala",
                     description="Chicken cooked in Marsala wine sauce with mushrooms",
                     price="7.95",
                     course="Entree",
                     restaurant=restaurant7)
app.session.add(menuItem2)
app.session.commit()

menuItem3 = MenuItem(user_id=3,
                     name="Potstickers",
                     description="Delicious chicken and veggies encapsulated in fried dough.",
                     price="6.50",
                     course="Appetizer",
                     restaurant=restaurant7)
app.session.add(menuItem3)
app.session.commit()

menuItem4 = MenuItem(user_id=1,
                     name="Nigiri Sampler",
                     description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
                     price="6.75",
                     course="Appetizer",
                     restaurant=restaurant7)
app.session.add(menuItem4)
app.session.commit()

menuItem5 = MenuItem(user_id=1,
                     name="Veggie Burger",
                     description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="7.00",
                     course="Entree",
                     restaurant=restaurant7)
app.session.add(menuItem5)
app.session.commit()

print "Added menu items!"
