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
                                    image_url varchar(3000) DEFAULT NULL,
                                    rcm_transport_id INTEGER DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS star_rating;")
cur.execute('''CREATE TABLE IF NOT EXISTS star_rating (comment_id INTEGER NOT NULL, 
                                    rate_id INTEGER DEFAULT NULL,
                                    star_number INTEGER DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS rcm_transport;")
cur.execute('''CREATE TABLE IF NOT EXISTS rcm_transport (rcm_transport_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    location_name varchar(300) DEFAULT NULL,
                                    train INTEGER DEFAULT 0,
                                    car INTEGER DEFAULT 0,
                                    ship INTEGER DEFAULT 0,
                                    motorbike INTEGER DEFAULT 0);''')

# restaurants
cur.execute("DROP TABLE IF EXISTS restaurants;")
cur.execute('''CREATE TABLE IF NOT EXISTS restaurants (restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    restaurant_name varchar(100) DEFAULT NULL,
                                    restaurant_address varchar(3000) DEFAULT NULL,
                                    hotel_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    restaurant_fee INTEGER DEFAULT NULL,
                                    restaurant_open_time varchar(1000) DEFAULT NULL,
                                    restaurant_description varchar(3000) DEFAULT NULL,
                                    menu_description varchar(3000) DEFAULT NULL,
                                    menu_img_url varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS hotels;")
cur.execute('''CREATE TABLE IF NOT EXISTS hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    hotel_name varchar(100) DEFAULT NULL,
                                    hotel_address varchar(3000) DEFAULT NULL,
                                    location_id INTEGER DEFAULT NULL,
                                    image_url varchar(1000) DEFAULT NULL,
                                    hotel_fee INTEGER DEFAULT NULL,
                                    hotel_description varchar(3000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS plans;")
cur.execute('''CREATE TABLE IF NOT EXISTS plans (plan_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    location_id INTEGER DEFAULT NULL,
                                    hotel_id INTEGER DEFAULT NULL,
                                    restaurant_id INTEGER DEFAULT NULL,
                                    user_id INTEGER DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS tags;")
cur.execute('''CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    tag_id INTEGER DEFAULT NULL,
                                    tag_name varchar(1000) DEFAULT NULL);''')

cur.execute("DROP TABLE IF EXISTS tags_loc;")
cur.execute('''CREATE TABLE IF NOT EXISTS tags_loc (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    tag_id INTEGER DEFAULT NULL,
                                    location_id INTEGER DEFAULT NULL);''')

cur.execute('''INSERT INTO users (user_id, name, email, password, image_url) VALUES
(1, 'hieu', 'hieu@gmail.com', 'hieu', 'http://halongcity.gov.vn/ckfinder/userfiles/images/2022/05/Loan/hanh/ltdl%20vinh%20HL.jpg'),
(2, 'admin', 'admin@gmail.com', 'admin', 'http://halongcity.gov.vn/ckfinder/userfiles/images/2022/05/Loan/hanh/ltdl%20vinh%20HL.jpg');''')

cur.execute('''INSERT INTO comments (comment_id, user_id, comment_content, comment_time, rate_id) VALUES
(1, 1, 'ngon', '1985‑09‑25 17:45:30.005', 1);''')

cur.execute('''INSERT INTO tourist_destination (location_id, location_name, location_description, location_address, image_url, rcm_transport_id) VALUES
(1, 'vinh ha long', 'bờ tây vịnh Bắc Bộ tại khu vực biển Đông Bắc Việt Nam', 'quang ninh', 'http://halongcity.gov.vn/ckfinder/userfiles/images/2022/05/Loan/hanh/ltdl%20vinh%20HL.jpg', 1),
(2, 'chua mot cot', 'Chùa Một Cột, Đội Cấn, Ba Đình, Hà Nội', 'ha noi', 'https://vietnam.travel/sites/default/files/styles/top_banner/public/2017-06/vietnam-travel-5.jpg?itok=XVnHP3ty', 2);''')

cur.execute('''INSERT INTO rcm_transport (rcm_transport_id, location_name, train, car, ship, motorbike) VALUES
(1, 'ha long', 1, 1, 1, 1),
(2, 'chua mot cot', 0, 1, 0, 1);''')

cur.execute('''INSERT INTO star_rating (comment_id, rate_id, star_number) VALUES
(1, 1, 5);''')

cur.execute('''INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_address, hotel_id, image_url, restaurant_fee, restaurant_open_time, restaurant_description,
menu_description, menu_img_url) VALUES
(1, 'Super Beau', 'so 18 duong Khong Biet', 1, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-IciUmCAz5cvDJf9fqRWKKUO0rxf0hLasCQ&usqp=CAU', 1500000, '8h-20h', 'restaurant description', 'menu des: khong ngon ko lay tien', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fthietkekhainguyen.com%2Fhinh-anh-giet-chet-ban-thiet-ke-menu%2F&psig=AOvVaw0JMshNn-copuLvk8NnZ_zN&ust=1671117235269000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCKjK4ZSz-fsCFQAAAAAdAAAAABAJ'),
(2, 'Hehe', 'so 18 duong Khong pho Troi', 2, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-IciUmCAz5cvDJf9fqRWKKUO0rxf0hLasCQ&usqp=CAU', 1000000, '8h-24h','hotel description', 'menu des: khong ngon van lay tien', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fthietkekhainguyen.com%2Fhinh-anh-giet-chet-ban-thiet-ke-menu%2F&psig=AOvVaw0JMshNn-copuLvk8NnZ_zN&ust=1671117235269000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCKjK4ZSz-fsCFQAAAAAdAAAAABAJ');''')

cur.execute('''INSERT INTO hotels (hotel_id, hotel_name, hotel_address, location_id, hotel_fee, image_url, hotel_description) VALUES
(1, 'Beau', 'so 18 duong Khong Biet', 1, 2000000, 'https://cdn.vietnambiz.vn/2019/11/4/dd32d9b188d86d6d8dc40d1ff9a0ebf6-15728512315071030248829.jpg', 'hotel description'),
(2, 'Beautyyyyyyyy', 'so 18 duong Khong pho Troi', 2, 1800000, 'https://cdn.vietnambiz.vn/2019/11/4/dd32d9b188d86d6d8dc40d1ff9a0ebf6-15728512315071030248829.jpg', 'hotel description');''')

cur.execute('''INSERT INTO plans (plan_id, location_id, hotel_id, restaurant_id, user_id) VALUES
(1, 1, 1, 1, 1),
(2, 2, 2, 2, 1);''')

con.commit()
con.close()
