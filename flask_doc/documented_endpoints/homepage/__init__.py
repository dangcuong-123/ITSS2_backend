from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('homepage', 'HomePage Information')


def responses(fetchdata, type):
    results = []
    if type == 'restaurants':
        keys = ['restaurant_id', 'restaurant_name',
                'hotel_id', 'image_url', 'restaurant_fee', 'restaurant_description']
    else:
        keys = ['hotel_id', 'hotel_name', 'location_id',
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
            return namespace.abort(404, 'Not Found')
        else:
            hotels = responses(hotels_query, 'hotels')
            restaurants = responses(restaurants_query, 'restaurants')
        print(hotels)
        print(restaurants)
        cur.close()
        return {'hotels':hotels, 'restaurants':restaurants}

parser_id = reqparse.RequestParser()
parser_id.add_argument('price', type=int, help='Hotel\'s price')
@namespace.route('/search_hotel_lower_equal_price', methods=['GET'])
class SearchByLowerPrice(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        price = request.args.get('price', default="NULL") #name = ao
        if(price == "NULL"):
            return namespace.abort(400, 'Invalid value')
            
        hotels_query = cur.execute(f'''select * from hotels as h
                        where h.hotel_fee <= {price};''').fetchall()
        if len(hotels_query) == 0:
            return namespace.abort(400, 'Not Found')

        hotels = responses(hotels_query, 'hotels')
        cur.close()
        return hotels

parser_id = reqparse.RequestParser()
parser_id.add_argument('price', type=int, help='Restaurant\'s price')
@namespace.route('/search_restaurant_lower_equal_price', methods=['GET'])
class SearchByLowerPrice(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_id)
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

parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Location\'s name (eg: ha long)')
@namespace.route('/search_name', methods=['GET'])
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
                                                    where location_name='{loc_name}'));''').fetchall()
        hotels_query = cur.execute(f'''select * from hotels as h
                        where h.location_id = (select location_id from tourist_destination
                                                    where location_name='{loc_name}');''').fetchall()
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
        return {'hotels':hotels, 'restaurants':restaurants}
    
