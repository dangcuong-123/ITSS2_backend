import json
from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('hotel', 'Hotels Information')


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

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('hotel_id', type=int,
                         help='Hotel\'s id (eg: 123)', location='json')
parser_edit.add_argument('hotel_name', type=str,
                         help='Hotel\'s name (eg: Beau)', location='json')
parser_edit.add_argument('hotel_description', type=str,
                         help='Hotel\'s detail (eg: rat la dep)', location='json')
parser_edit.add_argument('image_url', type=str,
                         help='Hotel\'s image', location='json')
parser_edit.add_argument('location_id', type=int,
                         help='Hotel\'s location id', location='json')

@namespace.route('/edit_hotel', methods=['PUT'])
class EditHotel(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID hotel Not Found - ID hotel Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        print(request.data)
        content = json.loads(request.data)
        hotel_id = content.get("hotel_id", "NULL")
        if(hotel_id == "NULL"):
            return namespace.abort(400, 'ID hotel Not Null')
        hotel_name = content.get('hotel_name', "NULL")
        hotel_description = content.get('hotel_description', "NULL")
        image_url = content.get('image_url', "NULL")
        location_id = content.get('location_id', "NULL")

        cur = con.cursor()
        cur.execute("SELECT hotel_id FROM hotels WHERE hotel_id = {};".format(
            hotel_id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Hotel Not Found')

        if(location_id != 'NULL'):
            cur.execute(
                "SELECT location_id FROM tourist_destination WHERE location_id = {};".format(location_id))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Location Not Found')

        cols = ['hotel_name', 'hotel_description', 'image_url']
        inputs = [hotel_name, hotel_description, image_url]
        for i, col in enumerate(cols):
            if(inputs[i] != "NULL"):
                cur.execute("UPDATE hotels SET {} = \"{}\" WHERE hotel_id = {};".format(
                    col, inputs[i], hotel_id))

        con.commit()
        cur.close()

        return 'Successfully Edit Hotel'


parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='hotel\'s id (eg: 123)')

@namespace.route('/delete_hotel', methods=['DELETE'])
class DeleteHotel(Resource):
    # @namespace.marshal_list_with(hotel_model)
    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully delete')
    @namespace.response(400, 'ID hotel not found')
    @namespace.expect(parser_delete)
    def delete(self):
        con = sqlite3.connect('database.db')
        id = request.args.get('id', default="NULL")
        print(id)
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        cur = con.cursor()
        cur.execute(
            "SELECT hotel_id FROM hotels WHERE hotel_id = {};".format(id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID hotel not found')

        cur.execute(
            "DELETE FROM hotels WHERE hotel_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete hotel'

@namespace.route('/show')
class ShowHotels(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        hotels_query = cur.execute(
            "SELECT * FROM hotels;").fetchall()
        if(len(hotels_query) == 0):
            return namespace.abort(400, 'Not Found')
        cur.close()

        return responses(hotels_query, 'hotels')


parser_hotels = reqparse.RequestParser()
parser_hotels.add_argument(
    'hotel_name', type=str, help='hotel name (eg: quan ngon)', location='json')
parser_hotels.add_argument(
    'location_id', type=str, help='location id', location='json')
parser_hotels.add_argument(
    'image_url', type=str, help='image hotels', location='json')
parser_hotels.add_argument(
    'hotel_description', type=str, help='hotel description', location='json')
@namespace.route('/create', methods=['POST'])
class CreateHotels(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_hotels, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        hotel_name = content.get("hotel_name", "NULL")
        location_id = content.get("location_id", "NULL")
        image_url = content.get("image_url")
        hotel_description = content.get("hotel_description")

        if(location_id != 'NULL'):
            cur.execute(
                "SELECT location_id FROM tourist_destination WHERE location_id = {};".format(location_id))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Location Not Found')

        hotel = (hotel_name, location_id,
                      image_url, hotel_description)
        sql = '''INSERT INTO hotels (hotel_name, location_id, 
            image_url, hotel_description) VALUES (?, ?, ?, ?);'''

        cur.execute(sql, hotel)
        con.commit()
        cur.close()

        return "create hotel successfully"

parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Hotel\'s name (eg: ha long)')
@namespace.route('/search_hotel_name', methods=['GET'])
class SearchByName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        hotel_name = request.args.get('name', default="NULL") #name = ao
        if(hotel_name == "NULL"):
            return namespace.abort(400, 'Invalid value')
        hotel_name = hotel_name.lower()
        hotels_query = cur.execute(f'''select * from hotels as h
                        where h.hotel_name like '%{hotel_name}%' COLLATE NOCASE;''').fetchall()

        if len(hotels_query) == 0:
            return namespace.abort(400, 'Not Found')

        hotels = responses(hotels_query, 'hotels')
        cur.close()
        return hotels
