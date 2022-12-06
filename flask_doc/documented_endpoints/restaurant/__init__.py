from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('restaurant', 'Restaurant Information')


def responses(fetchdata, type):
    results = []
    if type == 'restaurants':
        keys = ['restaurant_id', 'restaurant_name',
                'location_id', 'image_url', 'restaurant_description']
    else:
        keys = ['hotel_id', 'hotel_name', 'location_id',
                'image_url', 'hotel_description']
    for record in fetchdata:
        result = {}
        for x, i in enumerate(record):
            result[keys[x]] = i
        results.append(result)
    return results


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
