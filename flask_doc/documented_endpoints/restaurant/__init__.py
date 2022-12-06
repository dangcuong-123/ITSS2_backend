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
    'email', type=str, help='user\'s email (eg: hieu@gmail.com)', location='json')
parser_restaurants.add_argument(
    'password', type=str, help='Product\'s name (eg: quan dai)', location='json')


@namespace.route('/create')
class CreateRestaurants(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_restaurants, validate=True)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        restaurants_query = cur.execute(
            "SELECT * FROM restaurants;").fetchall()
        if(len(restaurants_query) == 0):
            return namespace.abort(404, 'Not Found')
        cur.close()

        return responses(restaurants_query, 'restaurants')
