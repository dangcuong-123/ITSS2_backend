import json
from flask import request, jsonify
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('restaurant', 'Restaurants Information')

def responses(fetchdata, type):
    results = []
    if type == 'restaurants':
        keys = ['restaurant_id', 'restaurant_name', 'restaurant_address', 'hotel_id',
        'image_url', 'restaurant_fee', 'restaurant_open_time', 'restaurant_description',
        'menu_description', 'menu_img_url']
    else:
        keys = ['hotel_id', 'hotel_name', 'hotel_address', 'location_id',
                'image_url', 'hotel_fee', 'hotel_description']
    for record in fetchdata:
        result = {}
        for x, i in enumerate(record):
            result[keys[x]] = i
        results.append(result)
    return results

parser_restaurants = reqparse.RequestParser()
parser_restaurants.add_argument(
    'restaurant_name', type=str, help='restaurant name (eg: quan ngon)', location='json')
parser_restaurants.add_argument(
    'restaurant_address_input', type=str, help='restaurant address input', location='json')
parser_restaurants.add_argument(
    'restaurant_address_select', type=str, help='restaurant address select', location='json')
parser_restaurants.add_argument(
    'hotel_id', type=str, help='hotel_id', location='json')
parser_restaurants.add_argument(
    'restaurant_fee', type=str, help='restaurants fee', location='json')
parser_restaurants.add_argument(
    'image_url', type=str, help='image restaurants', location='json')
parser_restaurants.add_argument(
    'restaurant_open_time', type=str, help='restaurant open time', location='json')
parser_restaurants.add_argument(
    'menu_img_url', type=str, help='Menu list', location='json')
parser_restaurants.add_argument(
    'menu_description', type=str, help='Menu list', location='json')
parser_restaurants.add_argument(
    'restaurant_description', type=str, help='restaurant description', location='json')
@namespace.route('/create', methods=['POST'])
class CreateRestaurants(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_restaurants, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        restaurant_name = content.get("restaurant_name", "NULL")
        restaurant_address_input = content.get("restaurant_address_input", "NULL")
        restaurant_address_select = content.get("restaurant_address_select", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_fee = content.get("restaurant_fee", "NULL")
        image_url = content.get("image_url", "NULL")
        restaurant_open_time = content.get("restaurant_open_time", "NULL")
        menu_img_url = content.get("menu_img_url", "NULL")
        menu_description = content.get("menu_description", "NULL")
        restaurant_description = content.get("restaurant_description", "NULL")

        if(hotel_id != 'NULL'):
            cur.execute(
                "SELECT hotel_id FROM hotels WHERE hotel_id = {};".format(hotel_id))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Hotel Not Found')
        
        restaurant_address = restaurant_address_input + ' ' + restaurant_address_select
        restaurant = (restaurant_name, restaurant_address, hotel_id, image_url,
                        restaurant_fee,restaurant_open_time, restaurant_description, menu_img_url, menu_description)
        sql = '''INSERT INTO restaurants (restaurant_name, restaurant_address, hotel_id, image_url, restaurant_fee,
        restaurant_open_time, restaurant_description, menu_img_url, menu_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        
        cur.execute(sql, restaurant)
        con.commit()
        cur.close()
        return "create restaurant successfully"

@namespace.route('/show')
class ShowRestaurants(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        restaurants_query = cur.execute(
            "SELECT * FROM restaurants;").fetchall()
        if(len(restaurants_query) == 0):
            return namespace.abort(400, 'Not Found')
        cur.close()

        return responses(restaurants_query, 'restaurants')


parser_edit = reqparse.RequestParser()
parser_edit.add_argument('restaurant_id', type=int,
                         help='Restaurant\'s id (eg: 123)', location='json')
parser_edit.add_argument(
    'restaurant_name', type=str, help='restaurant name (eg: quan ngon)', location='json')
parser_edit.add_argument(
    'restaurant_address_input', type=str, help='restaurant address input', location='json')
parser_edit.add_argument(
    'restaurant_address_select', type=str, help='restaurant address select', location='json')
parser_edit.add_argument(
    'hotel_id', type=str, help='hotel_id', location='json')
parser_edit.add_argument(
    'restaurant_fee', type=str, help='restaurants fee', location='json')
parser_edit.add_argument(
    'image_url', type=str, help='image restaurants', location='json')
parser_edit.add_argument(
    'restaurant_open_time', type=str, help='restaurant open time', location='json')
parser_edit.add_argument(
    'menu_img_url', type=str, help='Menu list', location='json')
parser_edit.add_argument(
    'menu_description', type=str, help='Menu list', location='json')
parser_edit.add_argument(
    'restaurant_description', type=str, help='restaurant description', location='json')
@namespace.route('/edit_restaurant', methods=['PUT'])
class EditRestaurant(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID Restaurant Not Found - ID Restaurant Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)
        restaurant_id = content.get("restaurant_id", "NULL")
        if(restaurant_id == "NULL"):
            return namespace.abort(400, 'ID Restaurant Not Null')
        restaurant_name = content.get("restaurant_name", "NULL")
        restaurant_address_input = content.get("restaurant_address_input", "NULL")
        restaurant_address_select = content.get("restaurant_address_select", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_fee = content.get("restaurant_fee", "NULL")
        image_url = content.get("image_url", "NULL")
        restaurant_open_time = content.get("restaurant_open_time", "NULL")
        menu_img_url = content.get("menu_img_url", "NULL")
        menu_description = content.get("menu_description", "NULL")
        restaurant_description = content.get("restaurant_description", "NULL")
        
        cur = con.cursor()
        cur.execute("SELECT restaurant_id FROM restaurants WHERE restaurant_id = {};".format(
            restaurant_id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Restaurant Not Found')

        if(hotel_id != 'NULL'):
            cur.execute(
                "SELECT hotel_id FROM hotels WHERE hotel_id = {};".format(hotel_id))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Hotel Not Found')

        restaurant_address = restaurant_address_input + ' ' + restaurant_address_select
        cols = ['restaurant_name', 'restaurant_address', 'hotel_id', 'image_url',
                    'restaurant_fee', 'restaurant_open_time', 'restaurant_description',
                    'menu_description', 'menu_img_url']
        inputs = [restaurant_name, restaurant_address, hotel_id, image_url,
                    restaurant_fee, restaurant_open_time, restaurant_description,
                    menu_description, menu_img_url]
        for i, col in enumerate(cols):
            if col == 'restaurant_address':
                if restaurant_address_input != None or restaurant_address_select != None:
                    cur.execute("UPDATE restaurants SET {} = \"{}\" WHERE restaurant_id = {};".format(
                        'restaurant_address', restaurant_address, restaurant_id))
            elif(inputs[i] != None):
                cur.execute("UPDATE restaurants SET {} = \"{}\" WHERE restaurant_id = {};".format(
                    col, inputs[i], restaurant_id))
        con.commit()
        cur.close()
        return 'Successfully Edit Restaurant'


parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='Restaurant\'s id (eg: 123)')
@namespace.route('/delete_restaurant', methods=['DELETE'])
class DeleteRestaurant(Resource):
    # @namespace.marshal_list_with(Restaurant_model)
    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully delete')
    @namespace.response(400, 'ID restaurant not found')
    @namespace.expect(parser_delete)
    def delete(self):
        con = sqlite3.connect('database.db')
        id = request.args.get('id', default="NULL")
        print(id)
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        cur = con.cursor()
        cur.execute(
            "SELECT restaurant_id FROM restaurants WHERE restaurant_id = {};".format(id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID restaurant not found')

        cur.execute(
            "DELETE FROM restaurants WHERE restaurant_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Restaurant'


parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Restaurant\'s name (eg: ha long)')
@namespace.route('/search_restaurant_name', methods=['GET'])
class SearchByName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        restaurant_name = request.args.get('name', default="NULL") #name = ao
        if(restaurant_name == "NULL"):
            return namespace.abort(400, 'Invalid value')
        restaurant_name = restaurant_name.lower()
        restaurants_query = cur.execute(f'''select * from restaurants as h
                        where h.restaurant_name like '%{restaurant_name}%' COLLATE NOCASE;''').fetchall()

        if len(restaurants_query) == 0:
            return namespace.abort(400, 'Not Found')

        hotels = responses(restaurants_query, 'restaurants')
        cur.close()
        return hotels

@namespace.route('/search_restaurant_id/<int:id>', methods=['GET'])
class SearchById(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    def get(self, id):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        restaurants_query = cur.execute(f'''select * from restaurants as h
                        where h.restaurant_id = {id};''').fetchall()
        if len(restaurants_query) == 0:
            return namespace.abort(400, 'Not Found')

        restaurants = responses(restaurants_query, 'restaurants')
        cur.close()
        return restaurants

parser_price = reqparse.RequestParser()
parser_price.add_argument('price', type=int, help='Restaurant\'s price')
@namespace.route('/search_restaurant_lower_equal_price', methods=['GET'])
class SearchByLowerPrice(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_price)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        price = request.args.get('price', default="NULL")
        if(price == "NULL"):
            return namespace.abort(400, 'Invalid value')
      
        restaurants_query = cur.execute(f'''select * from restaurants as r
                        where r.restaurant_fee <= {price};''').fetchall()
        if len(restaurants_query) == 0:
            return namespace.abort(400, 'Not Found')

        restaurants = responses(restaurants_query, 'restaurants')
        cur.close()
        return restaurants
