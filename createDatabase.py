import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()

# user
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    name varchar(50) DEFAULT NULL,
                                    email varchar(3000) DEFAULT NULL, 
                                    password varchar(50) DEFAULT NULL,
                                    image_url varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS comments;")
cur.execute('''CREATE TABLE IF NOT EXISTS comments (comment_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    user_id INTEGER DEFAULT NULL,
                                    comment_content varchar(3000) DEFAULT NULL,
                                    comment_time timestamp DEFAULT NULL,
                                    rate_id INTEGER DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS tourist_destination;")
cur.execute('''CREATE TABLE IF NOT EXISTS tourist_destination (location_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    location_name varchar(300) DEFAULT NULL,
                                    location_description varchar(3000) DEFAULT NULL,
                                    distance INTEGER DEFAULT NULL,
                                    image_url varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS star_rating;")
cur.execute('''CREATE TABLE IF NOT EXISTS star_rating (user_id INTEGER NOT NULL, 
                                    rate_id INTEGER DEFAULT NULL,
                                    star_number INTEGER DEFAULT NULL);''')

# restaurants
cur.execute("DROP TABLE IF EXISTS restaurants;")
cur.execute('''CREATE TABLE IF NOT EXISTS restaurants (restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    restaurant_name varchar(100) DEFAULT NULL,
                                    location_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    restaurant_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS hotels;")
cur.execute('''CREATE TABLE IF NOT EXISTS hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    hotel_name varchar(100) DEFAULT NULL,
                                    location_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    hotel_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS menu;")
cur.execute('''CREATE TABLE IF NOT EXISTS menu (menu_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    restaurant_id INTEGER DEFAULT NULL,
                                    hotel_name varchar(100) DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    menu_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS dishes;")
cur.execute('''CREATE TABLE IF NOT EXISTS dishes (dish_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    menu_id INTEGER DEFAULT NULL,
                                    dish_name varchar(100) DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    dish_price INTEGER DEFAULT NULL);''')


cur.execute('''INSERT INTO users (user_id, name, email, password, image_url) VALUES
(1, 'hieu', 'hieu@gmail.com', 'hieuhieu', 'sdfsdfsdfsdf');''')

cur.execute('''INSERT INTO comments (comment_id, user_id, comment_content, comment_time, rate_id) VALUES
(1, 1, 'ngon', '1985‑09‑25 17:45:30.005', 1);''')

cur.execute('''INSERT INTO tourist_destination (location_id, location_name, location_description, distance, image_url) VALUES
(1, 'ha long', 'rat la dep', 22, 'sdfsdfsdfsdfsd');''')

cur.execute('''INSERT INTO star_rating (user_id, rate_id, star_number) VALUES
(1, 1, 5);''')

cur.execute('''INSERT INTO restaurants (restaurant_id, restaurant_name, location_id, image_url, restaurant_description) VALUES
(1, 'Super Beau', 1, 'fsfsdfsdfsdfsdf', 'restaurant description');''')

cur.execute('''INSERT INTO hotels (hotel_id, hotel_name, location_id, image_url, hotel_description) VALUES
(1, 'Beau', 1, 'fsfsdfsdfsdfsdf', 'hotel description');''')

cur.execute('''INSERT INTO menu (menu_id, restaurant_id, hotel_name, image_url, menu_description) VALUES
(1, 1, 'Best sale', 'sdfsdfsdfsdf', 'very good');''')

cur.execute('''INSERT INTO dishes (dish_id, menu_id, dish_name, image_url, dish_price) VALUES
(1, 1, 'fry tofu', 'sdfsdfsdsdf', 100000);''')
con.commit()

con.close()