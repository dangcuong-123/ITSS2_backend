from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json
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
parser_name.add_argument('tags', type=str, help='''"[\"Reading\",\"Sketching\", \"Horse Riding\"]"''', location='json')
parser_name.add_argument('name', type=str, help='Location\'s name (eg: ha long)', location='json')
@namespace.route('/search_by_location_province_and_tags', methods=['POST'])
class SearchByNameTags(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        loc_name = content.get('name', "NULL") #name = ao
        tags_str = content.get('tags', "NULL") #name = ao
        if tags_str != "NULL":
            tags = json.loads(tags_str)

        if(loc_name != "NULL" and tags_str == 'NULL'):
            loc_name = loc_name.lower()
            restaurants_query = cur.execute(f'''select * from restaurants as r
                            where r.hotel_id in (select h.hotel_id from hotels as h
                                                        where h.location_id = (select location_id from tourist_destination
                                                        where loc_province like '%{loc_name}%' COLLATE NOCASE));''').fetchall()
            hotels_query = cur.execute(f'''select * from hotels as h
                            where h.location_id = (select location_id from tourist_destination
                                                        where loc_province like '%{loc_name}%' COLLATE NOCASE);''').fetchall()
            if(len(restaurants_query) == 0 and len(hotels_query) != 0):
                return responses(hotels_query, 'hotels')
            if(len(restaurants_query) != 0 and len(hotels_query) == 0):
                return responses(restaurants_query, 'restaurants')
            if(len(restaurants_query) == 0 and len(hotels_query) == 0):
                restaurants_query = cur.execute(f'''select * from restaurants as r
                            where r.hotel_id in (select h.hotel_id from hotels as h
                                                        where h.location_id = (select location_id from tourist_destination
                                                        where loc_province like '%{loc_name}%' COLLATE NOCASE));''').fetchall()
                hotels_query = cur.execute(f'''select * from hotels as h
                            where h.location_id = (select location_id from tourist_destination
                                                        where loc_province like '%{loc_name}%' COLLATE NOCASE);''').fetchall()
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
        if(loc_name == "NULL" and tags_str != 'NULL'):
            dict_loc_tag = {} 
            tags_query = cur.execute(f'''select * from tags_loc;''').fetchall()
            for loc_tag in tags_query:
                if loc_tag[1] not in dict_loc_tag.keys():
                    dict_loc_tag[loc_tag[1]] = [loc_tag[2]]
                else:
                    dict_loc_tag[loc_tag[1]].append(loc_tag[2])
            list_ok = [dict_loc_tag[tag] for tag in tags]
            rels = list(set(list_ok[0]).union(*list_ok))
            ress = []
            hots = []
            for rel in rels:
                restaurants_query = cur.execute(f'''select * from restaurants as r
                            where r.hotel_id in (select h.hotel_id from hotels as h
                                                        where h.location_id = (select location_id from tourist_destination
                                                        where location_id = {rel} ));''').fetchall()
                hotels_query = cur.execute(f'''select * from hotels as h
                            where h.location_id = (select location_id from tourist_destination
                                                        where location_id = {rel});''').fetchall()
                ress.extend(restaurants_query)
                hots.extend(hotels_query)
            
            hotels = responses(hots, 'hotels')
            restaurants = responses(ress, 'restaurants')
        if(loc_name != "NULL" and tags_str != 'NULL'):
            dict_loc_tag = {} 
            tags_query = cur.execute(f'''select * from tags_loc;''').fetchall()
            for loc_tag in tags_query:
                if loc_tag[1] not in dict_loc_tag.keys():
                    dict_loc_tag[loc_tag[1]] = [loc_tag[2]]
                else:
                    dict_loc_tag[loc_tag[1]].append(loc_tag[2])
            list_ok = [dict_loc_tag[tag] for tag in tags]
            list_ok_union = list(set(list_ok[0]).union(*list_ok))
            loc_name = loc_name.lower()
            loc_que = cur.execute(f'''select location_id from tourist_destination where loc_province like '%{loc_name}%' COLLATE NOCASE;''').fetchall()[0]
            loc_que = list(loc_que)
            merge = [list_ok_union,loc_que]
            rels = list(set(merge[0]).intersection(*merge))
            ress = []
            hots = []
            for rel in rels:
                restaurants_query = cur.execute(f'''select * from restaurants as r
                            where r.hotel_id in (select h.hotel_id from hotels as h
                                                        where h.location_id = (select location_id from tourist_destination
                                                        where location_id = {rel} ));''').fetchall()
                hotels_query = cur.execute(f'''select * from hotels as h
                            where h.location_id = (select location_id from tourist_destination
                                                        where location_id = {rel});''').fetchall()
                ress.extend(restaurants_query)
                hots.extend(hotels_query)

            hotels = responses(hots, 'hotels')
            restaurants = responses(ress, 'restaurants')

        cur.close()
        return {'hotels':hotels, 'restaurants':restaurants}
    
parser_name = reqparse.RequestParser()
parser_name.add_argument('tag_name', type=str, help='Tag\'s name (eg: ha long)')
@namespace.route('/search_by_tags', methods=['GET'])
class SearchByTags(Resource):
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
        return 'f'