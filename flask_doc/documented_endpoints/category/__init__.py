from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('category', 'Category related endpoints')

category_model = namespace.model('category', {
    'id': fields.Integer(
        readonly=True,
        description='This is id of category'
    ),
    'name': fields.String(
        readonly=True,
        description='Category\'s name'
    )
}, strict=True)

def responses(fetchdata):
    results = []
    keys = ['id', 'name']
    for j in fetchdata:
        result = {}
        for x, i in enumerate(j):
            result[keys[x]] = i
        results.append(result)
    return results

@namespace.route('/show')
class ShowCategory(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success', category_model)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM category")
        fetchdata = cur.fetchall()
        cur.close()
        if(len(fetchdata) == 0):
            return namespace.abort(404, 'Not Found')
        
        return responses(fetchdata)

parser_id = reqparse.RequestParser()
parser_id.add_argument('id', type=int, help='Category\'s id (eg: 5)')
@namespace.route('/id')
class SearchCategoryByID(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(400, 'Invalid value')
    @namespace.response(200, 'Success', category_model)

    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        id = request.args.get('id')
        if(name is None):
            return namespace.abort(400, 'Invalid value')
        cur.execute("SELECT * FROM category WHERE id = {}".format(id))
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)
        if(len(fetchdata) == 0):
            return namespace.abort(404, 'Not Found')
            # return 404
        
        return response


parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Category\'s name (eg: quan)')
@namespace.route('/name')
class SearchCategoryByName(Resource):
    # @namespace.marshal_list_with(product_model)
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(400, 'Invalid value')
    @namespace.response(200, 'Success', category_model)

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        name = request.args.get('name') #name = ao
        if(name is None):
            return namespace.abort(400, 'Invalid value')
            # return 400
        cur.execute("SELECT * FROM category WHERE name LIKE \"%{}%\" ".format(name))
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)
        if(len(fetchdata) == 0):
            return namespace.abort(404, 'Not Found')
        
        return response

parser_add = reqparse.RequestParser()
parser_add.add_argument('name', type=str, help='Category\'s name (eg: quan)', location='json')
@namespace.route('/add_category', methods=['PUT'])
class AddCategory(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully Added Category')
    @namespace.response(400, 'Category Already Exits')
    @namespace.expect(parser_add, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)

        name = content.get("name","NULL")
        
        cur = con.cursor()
        
        cur.execute("SELECT * FROM category WHERE name = \"{}\" ".format(name))
        fetchdata = cur.fetchall()
        if(len(fetchdata) != 0):
            cur.close()
            return namespace.abort(400, 'Category Already Exits')

        cur.execute("INSERT INTO category (name) VALUES (\"{}\");".format(name))
        con.commit()
        cur.close()
        return 'Successfully Added Category'

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='Category\'s id (eg: 123)', location='json')
@namespace.route('/delete_category', methods=['DELETE'])
class DeleteCategory(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully Delete Category')
    @namespace.response(400, 'ID not found')
    @namespace.expect(parser_delete, validate=True)
    def delete(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)

        id = content.get("id","NULL")

        cur = con.cursor()
        cur.execute("SELECT id FROM category WHERE id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID not found')

        cur.execute("DELETE FROM category WHERE id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Category'

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('id', type=int, help='Category\'s id (eg: 123)', location='json')
parser_edit.add_argument('name', type=str, help='New category\'s name (eg: quan)', location='json')
@namespace.route('/edit_category', methods=['POST'])
class EditCategory(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID Not Found')
    @namespace.response(200, 'Successfully Edit Category')
    @namespace.expect(parser_edit, validate=True)

    def post(self):
        con = sqlite3.connect('database.db')

        content = json.loads(request.data)

        id = content.get("id","NULL")

        if(id == "NULL"):
            return namespace.abort(400, 'Error')
        
        name = content.get("name", None)

        cur = con.cursor()
        cur.execute("SELECT id FROM category WHERE id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Category Not Found')

        cols = ['name']
        inputs = [name]
        for i, col in enumerate(cols):
            if(not inputs[i] is None):
                cur.execute("UPDATE category SET {} = \"{}\" WHERE id = {};".format(col, inputs[i], id))
        
        con.commit()
        cur.close()

        return 'Successfully Edit Category'


