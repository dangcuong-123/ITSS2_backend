from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('Homepage', 'HomePage Information')


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
class ShowHomePage(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        restaurants_query = cur.execute(
            "SELECT * FROM restaurants;").fetchall()
        hotels_query = cur.execute("SELECT * FROM hotels;").fetchall()

        if(len(restaurants_query) == 0 and len(hotels_query) != 0):
            return responses(hotels_query, 'hotels')
        if(len(restaurants_query) != 0 and len(hotels_query) == 0):
            return responses(restaurants_query, 'restaurants')
        if(len(restaurants_query) == 0 and len(hotels_query) == 0):
            return namespace.abort(404, 'Not Found')
        else:
            hotels = responses(hotels_query, 'hotels')
            restaurants = responses(restaurants_query, 'restaurants')

        cur.close()

        return {'hotels': hotels, 'restaurants': restaurants}
