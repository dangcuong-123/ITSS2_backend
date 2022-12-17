import json
from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3

namespace = Namespace('hotel', 'Hotels Information')

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

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('hotel_id', type=int,
                         help='Hotel\'s id (eg: 123)', location='json')
parser_edit.add_argument(
    'hotel_name', type=str, help='hotel name (eg: quan ngon)', location='json')
parser_edit.add_argument(
    'hotel_address_input', type=str, help='hotel address input (eg: 18 duong Vo Cong)', location='json')
parser_edit.add_argument(
    'hotel_address_select', type=str, help='hotel address select (eg: ha noi)', location='json')
parser_edit.add_argument(
    'image_url', type=str, help='image hotels', location='json')
parser_edit.add_argument(
    'hotel_description', type=str, help='hotel description', location='json')
parser_edit.add_argument(
    'hotel_fee', type=str, help='hotel description', location='json')
@namespace.route('/edit_hotel', methods=['PUT'])
class EditHotel(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID hotel Not Found - ID hotel Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)
        print(content)
        hotel_id = content.get("hotel_id", "NULL")
        if(hotel_id == "NULL"):
            return namespace.abort(400, 'ID hotel Not Null')
        hotel_name = content.get("hotel_name", "NULL")
        hotel_address_input = content.get("hotel_address_input", "NULL")
        hotel_address_select = content.get("hotel_address_select", "NULL")
        image_url = content.get("image_url", "NULL")
        print(image_url)
        hotel_description = content.get("hotel_description", "NULL")
        hotel_fee = content.get("hotel_fee", "NULL")

        cur = con.cursor()
        cur.execute("SELECT hotel_id FROM hotels WHERE hotel_id = {};".format(
            hotel_id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Hotel Not Found')

        if(hotel_address_select != None):
            cur.execute(
                "SELECT location_id FROM tourist_destination WHERE location_address like '%{}%';".format(hotel_address_select))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'Location Not Found')
            else:
                location_id = fetchdata[0][0]

        cols = ['hotel_name', 'hotel_address', 'location_id', 'hotel_fee', 'image_url', 'hotel_description']
        inputs = [hotel_name, hotel_address_input, location_id, hotel_fee, image_url, hotel_description]
        for i, col in enumerate(cols):
            if(inputs[i] != None):
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
    'hotel_address_input', type=str, help='hotel address input (eg: 18 duong Vo Cong)', location='json')
parser_hotels.add_argument(
    'hotel_address_select', type=str, help='hotel address select (eg: ha noi)', location='json')
parser_hotels.add_argument(
    'image_url', type=str, help='image hotels', location='json')
parser_hotels.add_argument(
    'hotel_description', type=str, help='hotel description', location='json')
parser_hotels.add_argument(
    'hotel_fee', type=str, help='hotel description', location='json')
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
        hotel_address_input = content.get("hotel_address_input", "NULL")
        hotel_address_select = content.get("hotel_address_select", "NULL")
        image_url = content.get("image_url")
        hotel_description = content.get("hotel_description")
        hotel_fee = content.get("hotel_fee")

        if(hotel_address_select != None):
            cur.execute(
                "SELECT location_id FROM tourist_destination WHERE location_address like '%{}%';".format(hotel_address_select))
            fetchdata = cur.fetchall()

            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'Location Not Found')
            else:
                location_id = fetchdata[0][0]
        hotel = (hotel_name, hotel_address_input, location_id, hotel_fee, image_url, hotel_description)
        sql = '''INSERT INTO hotels (hotel_name, hotel_address, location_id, hotel_fee, image_url, hotel_description) VALUES (?, ?, ?, ?, ?, ?);'''

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

@namespace.route('/search_hotel_id/<int:id>', methods=['GET'])
class SearchById(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    def get(self, id):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        hotels_query = cur.execute(f'''select * from hotels as h
                        where h.hotel_id = {id};''').fetchall()
        if len(hotels_query) == 0:
            return namespace.abort(400, 'Not Found')

        hotels = responses(hotels_query, 'hotels')
        cur.close()
        return hotels


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
                        where h.hotel_fee <= {price} order by h.hotel_fee DESC;''').fetchall()
        if len(hotels_query) == 0:
            return namespace.abort(400, 'Not Found')

        hotels = responses(hotels_query, 'hotels')
        cur.close()
        return hotels

parser_name = reqparse.RequestParser()
parser_name.add_argument('id', type=int, help='Hotel\'s id (eg: 1)')
@namespace.route('/get_restaurants_by_hotel_id', methods=['GET'])
class GetRestaurantsByHotelId(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        hotel_id = request.args.get('id', default="NULL") #name = ao
        if(hotel_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        restaurants_query = cur.execute(f'''select * from restaurants as r
                        where r.hotel_id = {hotel_id};''').fetchall()

        if len(restaurants_query) == 0:
            return namespace.abort(400, 'Not Found')

        restaurants = responses(restaurants_query, 'restaurants')
        cur.close()
        return restaurants