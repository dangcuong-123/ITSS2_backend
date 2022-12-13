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
                                    location_address varchar(3000) DEFAULT NULL,
                                    image_url varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS star_rating;")
cur.execute('''CREATE TABLE IF NOT EXISTS star_rating (comment_id INTEGER NOT NULL, 
                                    rate_id INTEGER DEFAULT NULL,
                                    star_number INTEGER DEFAULT NULL);''')

# restaurants
cur.execute("DROP TABLE IF EXISTS restaurants;")
cur.execute('''CREATE TABLE IF NOT EXISTS restaurants (restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    restaurant_name varchar(100) DEFAULT NULL,
                                    restaurant_address varchar(3000) DEFAULT NULL,
                                    hotel_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    restaurant_fee INTEGER DEFAULT NULL,
                                    restaurant_open_time varchar(1000) DEFAULT NULL,
                                    restaurant_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS hotels;")
cur.execute('''CREATE TABLE IF NOT EXISTS hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    hotel_name varchar(100) DEFAULT NULL,
                                    hotel_address varchar(3000) DEFAULT NULL,
                                    location_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    hotel_fee INTEGER DEFAULT NULL,
                                    hotel_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS menu;")
cur.execute('''CREATE TABLE IF NOT EXISTS menu (menu_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    restaurant_id INTEGER DEFAULT NULL,
                                    menu_description varchar(100) DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS dishes;")
cur.execute('''CREATE TABLE IF NOT EXISTS dishes (dish_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    menu_id INTEGER DEFAULT NULL,
                                    dish_name varchar(100) DEFAULT NULL,
                                    dish_price INTEGER DEFAULT NULL);''')


cur.execute('''INSERT INTO users (user_id, name, email, password, image_url) VALUES
(1, 'hieu', 'hieu@gmail.com', 'hieuhieu', 'data:image/jpeg;base64,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');''')

cur.execute('''INSERT INTO comments (comment_id, user_id, comment_content, comment_time, rate_id) VALUES
(1, 1, 'ngon', '1985‑09‑25 17:45:30.005', 1);''')

cur.execute('''INSERT INTO tourist_destination (location_id, location_name, location_description, location_address, image_url) VALUES
(1, 'ha long', 'rat la dep', 'quang ninh', 'http://halongcity.gov.vn/ckfinder/userfiles/images/2022/05/Loan/hanh/ltdl%20vinh%20HL.jpg'),
(2, 'chua mot cot', 'rat dep', 'ha noi', 'https://vietnam.travel/sites/default/files/styles/top_banner/public/2017-06/vietnam-travel-5.jpg?itok=XVnHP3ty');''')

cur.execute('''INSERT INTO star_rating (comment_id, rate_id, star_number) VALUES
(1, 1, 5);''')

cur.execute('''INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, hotel_id, image_url, restaurant_fee, restaurant_open_time, restaurant_description) VALUES
(1, 'Super Beau', 'so 18 duong Khong Biet', 1, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-IciUmCAz5cvDJf9fqRWKKUO0rxf0hLasCQ&usqp=CAU', 1500000, '8h-20h', 'restaurant description'),
(2, 'Hehe', 'so 18 duong Khong pho Troi', 2, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-IciUmCAz5cvDJf9fqRWKKUO0rxf0hLasCQ&usqp=CAU', 1000000, '8h-24h','hotel description');''')

cur.execute('''INSERT INTO hotels (hotel_id, hotel_name, hotel_address, location_id, hotel_fee, image_url, hotel_description) VALUES
(1, 'Beau', 'so 18 duong Khong Biet', 1, 2000000, 'https://cdn.vietnambiz.vn/2019/11/4/dd32d9b188d86d6d8dc40d1ff9a0ebf6-15728512315071030248829.jpg', 'hotel description'),
(2, 'Beautyyyyyyyy', 'so 18 duong Khong pho Troi', 2, 1800000, 'https://cdn.vietnambiz.vn/2019/11/4/dd32d9b188d86d6d8dc40d1ff9a0ebf6-15728512315071030248829.jpg', 'hotel description');''')

cur.execute('''INSERT INTO menu (menu_id, restaurant_id, image_url, menu_description) VALUES
(1, 1, 'data:image/jpeg;base64,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', 'very good');''')

cur.execute('''INSERT INTO dishes (dish_id, menu_id, dish_name, dish_price) VALUES
(1, 1, 'fry tofu', 100000);''')
con.commit()

con.close()
