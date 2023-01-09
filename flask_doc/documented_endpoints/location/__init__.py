from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json

namespace = Namespace('location', 'Location Information')


def responses(fetchdata, cur):
    results = []
    keys = ['location_id', 'location_name', 'location_description',
            'location_address', 'image_url', 'train', 'car', 'ship', 'motorbike']

    for idx, record in enumerate(fetchdata):
        transport_query = cur.execute(
            "SELECT * FROM rcm_transport WHERE rcm_transport_id={};".format(record[5])).fetchall()
        # print(transport_query[0][2])
        result = {}
        for x, i in enumerate(record):
            result[keys[x]] = i
        result['train'] = transport_query[0][2]
        result['car'] = transport_query[0][3]
        result['ship'] = transport_query[0][4]
        result['motorbike'] = transport_query[0][5]
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
    'location_name', type=int, help='location name (eg: ha long)', location='json')
parser_create.add_argument(
    'location_description', type=int, help='location description', location='json')
parser_create.add_argument(
    'location_address', type=int, help='location address (eg: quang ninh)', location='json')
parser_create.add_argument(
    'image_url', type=int, help='image url', location='json')
parser_create.add_argument(
    'train', type=int, help='train (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'car', type=int, help='car (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'ship', type=int, help='ship (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'motorbike', type=int, help='motorbike (eg: 0 or 1)', location='json')


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
        image_url = content.get("image_url", 'NULL')
        train = content.get("train", 'NULL')
        car = content.get("car", 'NULL')
        ship = content.get("ship", 'NULL')
        motorbike = content.get("motorbike", 'NULL')

        rcm_transport = (location_name, train, car, ship, motorbike)
        sql = '''INSERT INTO rcm_transport (location_name, train, car, ship, motorbike) VALUES (?, ?, ?, ?, ?);'''
        cur.execute(sql, rcm_transport)
        rcm_transport_id = cur.execute(
            '''SELECT rcm_transport_id FROM rcm_transport ORDER BY rcm_transport_id DESC LIMIT 1''').fetchall()[0][0]

        location = (location_name, location_description,
                    location_address, image_url, rcm_transport_id)
        sql = '''INSERT INTO tourist_destination (location_name, location_description,
                    location_address, image_url, rcm_transport_id) VALUES (?, ?, ?, ?, ?);'''

        cur.execute(sql, location)
        con.commit()
        cur.close()

        return "create location successfully"


parser_create = reqparse.RequestParser()
parser_create.add_argument(
    'location_id', type=int, help='location id (eg: 1)', location='json')
parser_create.add_argument(
    'location_name', type=int, help='location name (eg: ha long)', location='json')
parser_create.add_argument(
    'location_description', type=int, help='location description', location='json')
parser_create.add_argument(
    'location_address', type=int, help='location address (eg: quang ninh)', location='json')
parser_create.add_argument(
    'image_url', type=int, help='image url', location='json')
parser_create.add_argument(
    'train', type=int, help='train (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'car', type=int, help='car (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'ship', type=int, help='ship (eg: 0 or 1)', location='json')
parser_create.add_argument(
    'motorbike', type=int, help='motorbike (eg: 0 or 1)', location='json')


@namespace.route('/create', methods=['PUT'])
class EditLocation(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_create, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        location_id = content.get("location_id", "NULL")
        location_name = content.get("location_name", "NULL")
        location_description = content.get("location_description", "NULL")
        location_address = content.get("location_address", "NULL")
        image_url = content.get("image_url", 'NULL')
        train = content.get("train", 'NULL')
        car = content.get("car", 'NULL')
        ship = content.get("ship", 'NULL')
        motorbike = content.get("motorbike", 'NULL')

        # con.commit()
        cur.close()

        return "Edit location successfully"


parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='location\'s id (eg: 123)')


@namespace.route('/delete', methods=['DELETE'])
class CreateLocation(Resource):
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
        rcm_transport_id = fetchdata[0][1]
        cur.execute(
            "DELETE FROM rcm_transport WHERE rcm_transport_id={};".format(rcm_transport_id))

        cur.execute(
            "DELETE FROM tourist_destination WHERE location_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Location'
