import json
from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('restaurant', 'Restaurants Information')

def responses(fetchdata, type):
    results = []
    if type == 'restaurants':
        keys = ['restaurant_id', 'restaurant_name', 'location_id', 'image_url', 'restaurant_description']
    else:
        keys = ['hotel_id', 'hotel_name', 'location_id', 'image_url', 'hotel_description']
    for record in fetchdata:
        result = {}
        for x, i in enumerate(record):
            result[keys[x]] = i
        results.append(result)
    return results

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('restaurant_id', type=int, help='Restaurant\'s id (eg: 123)', location='json')
parser_edit.add_argument('restaurant_name', type=str, help='Restaurant\'s name (eg: Beau)', location='json')
parser_edit.add_argument('restaurant_description', type=str, help='Restaurant\'s detail (eg: rat la dep)', location='json')
parser_edit.add_argument('image_url', type=str, help='Restaurant\'s image', location='json')
parser_edit.add_argument('location_id', type=int, help='Restaurant\'s location id', location='json')
@namespace.route('/edit_restaurant', methods=['POST'])
class EditRestaurant(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID Restaurant Not Found - ID Restaurant Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)

    def post(self):
        con = sqlite3.connect('database.db')
        print(request.data)
        content = json.loads(request.data)
        restaurant_id = content.get("restaurant_id", "NULL")
        if(restaurant_id == "NULL"):
            return namespace.abort(400, 'ID Restaurant Not Null')
        restaurant_name = content.get('restaurant_name', "NULL")
        restaurant_description = content.get('restaurant_description', "NULL")
        image_url = content.get('image_url', "NULL")
        location_id = content.get('location_id', "NULL")

        cur = con.cursor()
        cur.execute("SELECT restaurant_id FROM restaurants WHERE restaurant_id = {};".format(restaurant_id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Restaurant Not Found')

        if(location_id != 'NULL'):
            cur.execute("SELECT location_id FROM tourist_destination WHERE location_id = {};".format(location_id))
            fetchdata = cur.fetchall()
            
            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Location Not Found')

        cols = ['restaurant_name', 'restaurant_description', 'image_url']
        inputs = [restaurant_name, restaurant_description, image_url]
        for i, col in enumerate(cols):
            if(inputs[i] != "NULL"):
                cur.execute("UPDATE restaurants SET {} = \"{}\" WHERE restaurant_id = {};".format(col, inputs[i], restaurant_id))
        
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
        cur.execute("SELECT restaurant_id FROM restaurants WHERE restaurant_id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID restaurant not found')

        cur.execute("DELETE FROM restaurants WHERE restaurant_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Restaurant'
    

@namespace.route('/show')
class ShowRestaurants(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        restaurants_query = cur.execute(
            "SELECT * FROM restaurants;").fetchall()
        if(len(restaurants_query) == 0):
            return namespace.abort(404, 'Not Found')
        cur.close()

        return responses(restaurants_query, 'restaurants')


parser_restaurants = reqparse.RequestParser()
parser_restaurants.add_argument(
    'restaurant_name', type=str, help='restaurant name (eg: quan ngon)', location='json')
parser_restaurants.add_argument(
    'location_id', type=str, help='location id', location='json')
parser_restaurants.add_argument(
    'image_url', type=str, help='image restaurants', location='json')
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
        location_id = content.get("location_id", "NULL")
        image_url = content.get("image_url")
        restaurant_description = content.get("restaurant_description")
        restaurant = (restaurant_name, location_id,
                      image_url, restaurant_description)
        sql = '''INSERT INTO restaurants (restaurant_name, location_id, 
            image_url, restaurant_description) VALUES (?, ?, ?, ?);'''

        cur.execute(sql, restaurant)
        con.commit()
        cur.close()

        return "create restaurant successfully"
