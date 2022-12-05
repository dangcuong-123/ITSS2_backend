from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('homepage', 'HomePage Information')


def responses(fetchdata):
    results = []
    keys = ['restaurant_id', 'restaurant_name', 'restaurant_location_id', 'restaurant_image_url', 'restaurant_description',
            'hotel_id', 'hotel_name', 'hotel_location_id', 'hotel_image_url', 'hotel_description']
    for j in fetchdata:
        result = {}
        for x, i in enumerate(j):
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
        cur.execute("SELECT * FROM restaurants, hotels;")
        fetchdata = cur.fetchall()
        cur.close()
        if(len(fetchdata) == 0):
            return namespace.abort(404, 'Not Found')
        print(fetchdata)
        return responses(fetchdata)
