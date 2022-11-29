from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('product', 'Product related endpoints')

product_model = namespace.model('product', {
    'id': fields.Integer(
        readonly=True,
        description='This is id of products'
    ),
    'name': fields.String(
        readonly=True,
        description='Product\'s name'
    ),
    'detail': fields.String(
        readonly=True,
        description='Product\'s detail'
    ),
    'brand': fields.String(
        readonly=True,
        description='Product\'s brand'
    ),
    'price': fields.Float(
        readonly=True,
        description='Product\'s price'
    ),
    'category_id': fields.Integer(
        readonly=True,
        description='Product\'s category_id'
    ),
    'image': fields.String(
        readonly=True,
        description='Product\'s image'
    ),
    'size': fields.String(
        readonly=True,
        description='Product\'s size'
    ),
    'video': fields.String(
        readonly=True,
        description='Product\'s video'
    ),
    'color': fields.String(
        readonly=True,
        description='Product\'s color'
    ),    
    'quantity': fields.Integer(
        readonly=True,
        description='Product\'s quantity'
    )
}, strict=True)

def responses(fetchdata):
    results = []
    keys = ['id', 'name', 'detail', 'brand', 'price','category_id', 'image',
            'size', 'video', 'color', 'quantity']
    for j in fetchdata:
        result = {}
        for x, i in enumerate(j):
            result[keys[x]] = i
        results.append(result)
    return results

@namespace.route('/show')
class ShowProduct(Resource):

    # @namespace.marshal_list_with(product_model)
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success', product_model)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM products")
        fetchdata = cur.fetchall()
        cur.close()
        if(len(fetchdata) == 0):
            return namespace.abort(400, 'Not Found')
            # return 404
        
        return responses(fetchdata)

parser_id = reqparse.RequestParser()
parser_id.add_argument('id', type=int, help='Product\'s id (eg: 5)')
@namespace.route('/id')
class SearchByID(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success', product_model)

    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        id = request.args.get('id', default="NULL") #name = ao
        if(id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        cur.execute("SELECT * FROM products WHERE id = {}".format(id))
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)
        if(len(fetchdata) == 0):
            return namespace.abort(400, 'Not Found')
        
        return response


parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=str, help='Product\'s name (eg: quan)')
@namespace.route('/name')
class SearchByName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success', product_model)

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        name = request.args.get('name') #name = ao
        if(name is None):
            return namespace.abort(400, 'Invalid value')
            # return 400
        cur.execute("SELECT * FROM products WHERE name LIKE \"%{}%\"".format(name))
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)
        if(len(fetchdata) == 0):
            return namespace.abort(400, 'Not Found')
        
        return response

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


parser_price = reqparse.RequestParser()
parser_price.add_argument('from', type=float, help='Price product\'s from (eg: 100)')
parser_price.add_argument('to', type=float, help='Price product\'s to (eg: 200)')
@namespace.route('/price')
class SearchByPrice(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - From and to must be numberic - From must be less than to - Not Found')
    @namespace.response(200, 'Success', product_model)
    @namespace.expect(parser_price)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        froms = request.args.get('from') 
        tos = request.args.get('to') 
        if(froms is None or tos is None):
            return namespace.abort(400, 'Invalid value')

        if(not is_float(tos) or not is_float(froms)):
            # response = 250
            return namespace.abort(400, 'from and to must be numberic')
            
        tos = float(tos)
        froms = float(froms)
        if(tos < froms):
            return namespace.abort(400, 'From must be less than to')
        cur.execute("SELECT * FROM products WHERE {} > price AND price > {}".format(tos, froms))
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)
        if(fetchdata == ()):
            return namespace.abort(400, 'Not Found')
        return response


parser_filter = reqparse.RequestParser()
parser_filter.add_argument('category_id', type=int, help='Product\'s category id (eg: 128)')
parser_filter.add_argument('size', type=str, help='Product\'s size (eg: A)')
parser_filter.add_argument('color', type=str, help='Product\'s color (eg: vang)')
@namespace.route('/filters')
class SearchByFilters(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success', product_model)
    @namespace.expect(parser_filter)
    def get(self):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        category = request.args.get('category_id')
        size = request.args.get('size')
        color = request.args.get('color')
        
        if((not category is None) and (not size is None) and (not color is None)): 
            cur.execute("SELECT * FROM products WHERE category_id = \"{}\" AND size = \"{}\" AND color LIKE \"%{}%\"".format(category, size, color))

        elif((not size is None) and (not category is None)):
            cur.execute("SELECT * FROM products WHERE category_id = \"{}\" AND size = \"{}\" ".format(category, size))

        elif((not category is None) and (not color is None)):
            cur.execute("SELECT * FROM products WHERE category_id = \"{}\" AND color LIKE \"%{}%\" ".format(category, color))
        
        elif((not size is None) and (not color is None)):
            cur.execute("SELECT * FROM products WHERE size = \"{}\" AND color LIKE \"%{}%\" ".format(size, color))

        elif(not category is None):
            cur.execute("SELECT p.* FROM products p,category c WHERE category_id = \"{}\"".format(category))

        elif(not size is None):
            cur.execute("SELECT * FROM products WHERE size = \"{}\"".format(size))

        elif(not color is None):
            cur.execute("SELECT * FROM products WHERE color LIKE \"%{}%\"".format(color))

        
        fetchdata = cur.fetchall()
        cur.close()
        response = responses(fetchdata)

        if(len(fetchdata) == 0):
            return namespace.abort(400, 'Not Found')
        return response


parser_add = reqparse.RequestParser()
parser_add.add_argument('name', type=str, help='Product\'s name (eg: quan dai)', location='form')
parser_add.add_argument('detail', type=str, help='Product\'s detail (eg: vai den tron bong)', location='form')
parser_add.add_argument('brand', type=str, help='Product\'s brand', location='form')
parser_add.add_argument('price', type=float, help='Product\'s price (eg: 50000)', location='form')
parser_add.add_argument('category_id', type=int, help='Product\'s category_id', location='form')
parser_add.add_argument('image', type=str, help='Product\'s image (eg: fgfg)', location='form')
parser_add.add_argument('size', type=str, help='Product\'s size (eg: M)', location='form')
parser_add.add_argument('video', type=str, help='Product\'s video (eg: dfg)', location='form')
parser_add.add_argument('color', type=str, help='Product\'s color (eg: den)', location='form')
parser_add.add_argument('quantity', type=int, help='Product\'s quantity (eg: 5)', location='form')
@namespace.route('/add_product', methods=['PUT'])
class AddProduct(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'ID category not found')
    @namespace.response(200, 'Successfully Added')
    @namespace.expect(parser_add, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        name = request.form.get('name', default="NULL")
        detail = request.form.get('detail', default="NULL")
        brand = request.form.get('brand', default="NULL")
        price = request.form.get('price', default="NULL")
        category_id = request.form.get('category_id', default="NULL")
        image = request.form.get('image', default="NULL")
        size = request.form.get('size', default="NULL")
        video = request.form.get('video', default="NULL")
        color = request.form.get('color', default="NULL")
        quantity = request.form.get('quantity', default="NULL")
        
        cur = con.cursor()

        cur.execute("SELECT * FROM category WHERE id = {}".format(category_id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID category not found')
        
        cur.execute("INSERT INTO products (name, detail, brand, price, category_id, image, size, video, color, quantity) VALUES (\"{}\", \"{}\", \"{}\", {}, {}, \"{}\", \"{}\", \"{}\", \"{}\", {});".format
                    (name, detail, brand, price, category_id, image, size, video, color, quantity))
        con.commit()
        cur.close()
        return 'Successfully Added Product'

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='Product\'s id (eg: 123)', location='form')
@namespace.route('/delete_product', methods=['DELETE'])
class DeleteProduct(Resource):

    # @namespace.marshal_list_with(product_model)
    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully delete')
    @namespace.response(400, 'ID product not found')
    @namespace.expect(parser_delete, validate=True)
    def delete(self):
        con = sqlite3.connect('database.db')

        id = request.form['id']

        cur = con.cursor()
        cur.execute("SELECT id FROM products WHERE id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID product not found')

        cur.execute("DELETE FROM products WHERE id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Product'

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('id', type=int, help='Product\'s id (eg: 123)', location='form')
parser_edit.add_argument('name', type=str, help='Product\'s name (eg: quan dai)', location='form')
parser_edit.add_argument('detail', type=str, help='Product\'s detail (eg: vai den tron bong)', location='form')
parser_edit.add_argument('brand', type=str, help='Product\'s brand', location='form')
parser_edit.add_argument('price', type=float, help='Product\'s price (eg: 50000)', location='form')
parser_edit.add_argument('category_id', type=int, help='Product\'s category_id', location='form')
parser_edit.add_argument('image', type=str, help='Product\'s image (eg: fgfg)', location='form')
parser_edit.add_argument('size', type=str, help='Product\'s size (eg: M)', location='form')
parser_edit.add_argument('video', type=str, help='Product\'s video (eg: dfg)', location='form')
parser_edit.add_argument('color', type=str, help='Product\'s color (eg: den)', location='form')
parser_edit.add_argument('quantity', type=int, help='Product\'s quantity (eg: 5)', location='form')
@namespace.route('/edit_product', methods=['POST'])
class EditProduct(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID Product Not Found - ID Product Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)

    def post(self):
        con = sqlite3.connect('database.db')
        
        id = request.form.get("id", default="NULL")
        if(id == "NULL"):
            return namespace.abort(400, 'ID Product Not Null')
        name = request.form.get('name', default="NULL")
        detail = request.form.get('detail', default="NULL")
        brand = request.form.get('brand', default="NULL")
        price = request.form.get('price', default="NULL")
        category_id = request.form.get('category_id', default="NULL")
        image = request.form.get('image', default="NULL")
        size = request.form.get('size', default="NULL")
        video = request.form.get('video', default="NULL")
        color = request.form.get('color', default="NULL")
        quantity = request.form.get('quantity', default="NULL")

        cur = con.cursor()
        cur.execute("SELECT id FROM products WHERE id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Product Not Found')
        print(category_id)
        if(category_id != 'NULL'):
            cur.execute("SELECT id FROM category WHERE id = {};".format(category_id))
            fetchdata = cur.fetchall()
            
            if(len(fetchdata) == 0):
                cur.close()
                return namespace.abort(400, 'ID Category Not Found')

        cols = ['name', 'detail', 'brand', 'price', 'category_id', 'image', 'size', 'video', 'color', 'quantity']
        inputs = [name, detail, brand, price, category_id, image, size, video, color, quantity]
        for i, col in enumerate(cols):
            if(inputs[i] != "NULL"):
                cur.execute("UPDATE products SET {} = \"{}\" WHERE id = {};".format(col, inputs[i], id))
        
        con.commit()
        cur.close()

        return 'Successfully Edit Product'

