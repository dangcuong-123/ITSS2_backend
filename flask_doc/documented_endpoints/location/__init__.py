from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json

namespace = Namespace('location', 'Location Information')


def responses(fetchdata, cur):
    results = []
    keys = ['location_id', 'location_name', 'location_description',
            'location_address', 'image_url', 'tags', 'loc_province', 'train', 'car', 'ship', 'motorbike']

    for idx, record in enumerate(fetchdata):
        result = {}
        for x, i in enumerate(record):
            result[keys[x]] = i
        tags_query = cur.execute(
            "SELECT * FROM tags_loc WHERE tags_loc.location_id={};".format(record[0])).fetchall()
        if(len(tags_query) != 0):
            result['tags'] = [tag[1] for tag in tags_query]
        else:
            result['tags'] = []
        transport_query = cur.execute(
            "SELECT * FROM rcm_transport WHERE rcm_transport_id={};".format(record[5])).fetchall()
        result['train'] = transport_query[0][1]
        result['car'] = transport_query[0][2]
        result['ship'] = transport_query[0][3]
        result['motorbike'] = transport_query[0][4]
        results.append(result)
    return results


@namespace.route('/show', methods=['GET'])
class ShowLocation(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plans_query = cur.execute(
            "SELECT * FROM tourist_destination;").fetchall()
        if(len(plans_query) == 0):
            return namespace.abort(400, 'Not Found')
        respon = responses(plans_query, cur)
        cur.close()
        return respon


parser_create = reqparse.RequestParser()
parser_create.add_argument(
    'location_name', type=str, help='location name (eg: ha long)', location='json')
parser_create.add_argument(
    'location_description', type=str, help='location description', location='json')
parser_create.add_argument(
    'location_address', type=str, help='location address (eg: quang ninh)', location='json')
parser_create.add_argument(
    'loc_province', type=str, help='location address (eg: quang ninh)', location='json')
parser_create.add_argument(
    'image_url', type=str, help='image url', location='json')
parser_create.add_argument(
    'train', type=int, help='train (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'car', type=int, help='car (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'ship', type=int, help='ship (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'motorbike', type=int, help='motorbike (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'tags', type=str, help='''"[\"Reading\",\"Sketching\", \"Horse Riding\"]"''', location='json')

@namespace.route('/create', methods=['POST'])
class CreateLocation(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_create, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        location_name = content.get("location_name", "NULL")
        location_description = content.get("location_description", "NULL")
        location_address = content.get("location_address", "NULL")
        loc_province = content.get("loc_province", "NULL")
        image_url = content.get("image_url", 'NULL')
        train = content.get("train", 'NULL')
        car = content.get("car", 'NULL')
        ship = content.get("ship", 'NULL')
        motorbike = content.get("motorbike", 'NULL')
        tags_str = content.get("tags", 'NULL')

        rcm_transport_id = cur.execute(
            f'''SELECT rcm_transport_id FROM rcm_transport WHERE train={train} and car={car} and ship={ship} and motorbike={motorbike}''').fetchall()[0][0]

        location = (location_name, location_description,
                    location_address, image_url, rcm_transport_id, loc_province)
        sql = '''INSERT INTO tourist_destination (location_name, location_description,
                    location_address, image_url, rcm_transport_id, loc_province) VALUES (?, ?, ?, ?, ?, ?);'''
        cur.execute(sql, location)

        location_id = cur.execute(
            '''SELECT location_id FROM tourist_destination ORDER BY location_id DESC LIMIT 1''').fetchall()[0][0]
        tags = json.loads(tags_str)
        for tag in tags:
            tag_loc = (tag, location_id)
            sql = '''INSERT INTO tags_loc (tag_name, location_id) VALUES (?, ?);'''
            cur.execute(sql, tag_loc)
        con.commit()
        cur.close()

        return "create location successfully"


parser_edit = reqparse.RequestParser()
parser_edit.add_argument(
    'location_id', type=int, help='location id (eg: 1)', location='json')
parser_edit.add_argument(
    'location_name', type=str, help='location name (eg: ha long)', location='json')
parser_edit.add_argument(
    'location_description', type=str, help='location description', location='json')
parser_edit.add_argument(
    'location_address', type=str, help='location address (eg: quang ninh)', location='json')
parser_edit.add_argument(
    'loc_province', type=str, help='location address (eg: quang ninh)', location='json')
parser_edit.add_argument(
    'image_url', type=str, help='image url', location='json')
parser_edit.add_argument(
    'train', type=int, help='train (eg: 0 or 1)', location='json')
parser_edit.add_argument(
    'car', type=int, help='car (eg: 0 or 1)', location='json')
parser_edit.add_argument(
    'ship', type=int, help='ship (eg: 0 or 1)', location='json')
parser_edit.add_argument(
    'motorbike', type=int, help='motorbike (eg: 0 or 1)', location='json')
parser_edit.add_argument(
    'tags', type=str, help='''"[\"Reading\",\"Sketching\", \"Horse Riding\"]"''', location='json')


@namespace.route('/edit', methods=['PUT'])
class EditLocation(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_edit, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        location_id = content.get("location_id", "NULL")
        location_name = content.get("location_name", "NULL")
        location_description = content.get("location_description", "NULL")
        location_address = content.get("location_address", "NULL")
        loc_province = content.get("loc_province", "NULL")
        image_url = content.get("image_url", 'NULL')
        train = content.get("train", 'NULL')
        car = content.get("car", 'NULL')
        ship = content.get("ship", 'NULL')
        motorbike = content.get("motorbike", 'NULL')
        tags_str = content.get("tags", 'NULL')
        rcm_transport_id = cur.execute(
            f'''SELECT rcm_transport_id FROM rcm_transport WHERE train={train} and car={car} and ship={ship} and motorbike={motorbike}''').fetchall()[0][0]

        cur.execute(f'''UPDATE tourist_destination SET location_name="{location_name}", location_description='{location_description}',
                    location_address='{location_address}', image_url='{image_url}', rcm_transport_id={rcm_transport_id}, loc_province='{loc_province}'
                    WHERE location_id={location_id};''')
        cur.execute(f"DELETE FROM tags_loc WHERE location_id={location_id};")
        tags = json.loads(tags_str)
        for tag in tags:
            tag_loc = (tag, location_id)
            sql = '''INSERT INTO tags_loc (tag_name, location_id) VALUES (?, ?);'''
            cur.execute(sql, tag_loc)

        con.commit()
        cur.close()

        return "Edit location successfully"


parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='location\'s id (eg: 123)')


@namespace.route('/delete', methods=['DELETE'])
class DeleteLocation(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_delete, validate=True)
    def delete(self):
        con = sqlite3.connect('database.db')
        id = request.args.get('id', default="NULL")
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        cur = con.cursor()
        cur.execute(
            "SELECT location_id, rcm_transport_id FROM tourist_destination WHERE location_id = {};".format(id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID location not found')

        cur.execute(
            "DELETE FROM tourist_destination WHERE location_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Location'


@namespace.route('/get_tags_name', methods=['GET'])
class GetTagsName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect()
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        tags_query = cur.execute(f'''select * from tags;''').fetchall()

        cur.close()
        return [tag[1] for tag in tags_query]


parser_name = reqparse.RequestParser()
parser_name.add_argument(
    'name', type=str, help='location\'s name or province (eg: ha noi)')


@namespace.route('/search_location_by_name_and_province', methods=['GET'])
class SearchByNameProvince(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_name, validate=True)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        name = request.args.get('name', default="NULL")
        locs_query = cur.execute(
            f'''select * from tourist_destination where location_name like "%{name}%" or loc_province like "%{name}%";''').fetchall()
        if(len(locs_query) == 0):
            return namespace.abort(400, 'Not Found')
        respon = responses(locs_query, cur)
        cur.close()
        return respon


# parser_id = reqparse.RequestParser()
# parser_id.add_argument('location_id', type=int, help='Location id')


@namespace.route('/get_location_by_id/<location_id>')
class GetLocationById(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    # @namespace.expect(parser_id)
    def get(self, location_id):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        # location_id = request.args.get(
        #     'location_id', default="NULL")  # name = ao
        if(location_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        location_query = cur.execute(
            f'select * from tourist_destination where location_id={location_id};').fetchall()
        if(len(location_query) == 0):
            return namespace.abort(400, 'Location Not Exists')

        respon = responses(location_query, cur)
        cur.close()
        return respon[0]
