from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('homepage', 'HomePage Information')

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
            return namespace.abort(400, 'Not Found')
        else:
            hotels = responses(hotels_query, 'hotels')
            restaurants = responses(restaurants_query, 'restaurants')

        cur.close()
        return {'hotels':hotels, 'restaurants':restaurants}


parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Location\'s name (eg: ha long)')
@namespace.route('/search_location_name', methods=['GET'])
class SearchByName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        loc_name = request.args.get('name', default="NULL") #name = ao
        if(loc_name == "NULL"):
            return namespace.abort(400, 'Invalid value')
        loc_name = loc_name.lower()
        restaurants_query = cur.execute(f'''select * from restaurants as r
                        where r.hotel_id in (select h.hotel_id from hotels as h
                                                    where h.location_id = (select location_id from tourist_destination
                                                    where location_name like '%{loc_name}%' COLLATE NOCASE));''').fetchall()
        hotels_query = cur.execute(f'''select * from hotels as h
                        where h.location_id = (select location_id from tourist_destination
                                                    where location_name like '%{loc_name}%' COLLATE NOCASE);''').fetchall()
        if(len(restaurants_query) == 0 and len(hotels_query) != 0):
            return responses(hotels_query, 'hotels')
        if(len(restaurants_query) != 0 and len(hotels_query) == 0):
            return responses(restaurants_query, 'restaurants')
        if(len(restaurants_query) == 0 and len(hotels_query) == 0):
            restaurants_query = cur.execute(f'''select * from restaurants as r
                        where r.hotel_id in (select h.hotel_id from hotels as h
                                                    where h.location_id = (select location_id from tourist_destination
                                                    where location_address like '%{loc_name}%' COLLATE NOCASE));''').fetchall()
            hotels_query = cur.execute(f'''select * from hotels as h
                        where h.location_id = (select location_id from tourist_destination
                                                    where location_address like '%{loc_name}%' COLLATE NOCASE);''').fetchall()
            if(len(restaurants_query) == 0 and len(hotels_query) != 0):
                return responses(hotels_query, 'hotels')
            if(len(restaurants_query) != 0 and len(hotels_query) == 0):
                return responses(restaurants_query, 'restaurants')
            if(len(restaurants_query) == 0 and len(hotels_query) == 0):
                return namespace.abort(400, 'Not Found')
            else:
                hotels = responses(hotels_query, 'hotels')
                restaurants = responses(restaurants_query, 'restaurants')
        else:
            hotels = responses(hotels_query, 'hotels')
            restaurants = responses(restaurants_query, 'restaurants')

        cur.close()
        return {'hotels':hotels, 'restaurants':restaurants}
    
