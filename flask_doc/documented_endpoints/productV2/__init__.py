from os import name
from flask import request, json
from flask_restx import Namespace, Resource, fields, reqparse
import sqlite3

namespace = Namespace('productV2', 'Product related endpoints')

product_model = namespace.model('productV2', {
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


parser_add = reqparse.RequestParser()
parser_add.add_argument('name', type=str, help='Product\'s name (eg: quan dai)', location='json')
parser_add.add_argument('detail', type=str, help='Product\'s detail (eg: vai den tron bong)', location='json')
parser_add.add_argument('brand', type=str, help='Product\'s brand', location='json')
parser_add.add_argument('price', type=float, help='Product\'s price (eg: 50000)', location='json')
parser_add.add_argument('category_id', type=int, help='Product\'s category_id', location='json')
parser_add.add_argument('image', type=str, help='Product\'s image (eg: fgfg)', location='json')
parser_add.add_argument('size', type=str, help='Product\'s size (eg: M)', location='json')
parser_add.add_argument('video', type=str, help='Product\'s video (eg: dfg)', location='json')
parser_add.add_argument('color', type=str, help='Product\'s color (eg: den)', location='json')
parser_add.add_argument('quantity', type=int, help='Product\'s quantity (eg: 5)', location='json')
@namespace.route('/add_product', methods=['PUT'])
class AddProduct(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'ID category not found')
    @namespace.response(200, 'Successfully Added')
    @namespace.expect(parser_add, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)
        name = content.get("name","NULL")
        detail = content.get("detail","NULL")
        brand = content.get("brand","NULL")
        price = content.get("price","NULL")
        category_id = content.get("category_id","NULL")
        image = content.get("image","NULL")
        size = content.get("size","NULL")
        video = content.get("video","NULL")
        color = content.get("color","NULL")
        quantity = content.get("quantity","NULL")
        
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
parser_delete.add_argument('id', type=int, help='Product\'s id (eg: 123)', location='json')
@namespace.route('/delete_product', methods=['DELETE'])
class DeleteProduct(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(200, 'Successfully delete')
    @namespace.response(400, 'ID product not found')
    @namespace.expect(parser_delete, validate=True)
    def delete(self):
        con = sqlite3.connect('database.db')

        content = json.loads(request.data)
        id = content.get("id","NULL")

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
parser_edit.add_argument('id', type=int, help='Product\'s id (eg: 123)', location='json')
parser_edit.add_argument('name', type=str, help='Product\'s name (eg: quan dai)', location='json')
parser_edit.add_argument('detail', type=str, help='Product\'s detail (eg: vai den tron bong)', location='json')
parser_edit.add_argument('brand', type=str, help='Product\'s brand', location='json')
parser_edit.add_argument('price', type=float, help='Product\'s price (eg: 50000)', location='json')
parser_edit.add_argument('category_id', type=int, help='Product\'s category_id', location='json')
parser_edit.add_argument('image', type=str, help='Product\'s image (eg: fgfg)', location='json')
parser_edit.add_argument('size', type=str, help='Product\'s size (eg: M)', location='json')
parser_edit.add_argument('video', type=str, help='Product\'s video (eg: dfg)', location='json')
parser_edit.add_argument('color', type=str, help='Product\'s color (eg: den)', location='json')
parser_edit.add_argument('quantity', type=int, help='Product\'s quantity (eg: 5)', location='json')
@namespace.route('/edit_product', methods=['POST'])
class EditProduct(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID Product Not Found - ID Product Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)

    def post(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)

        id = content.get("id","NULL")
        if(id == "NULL"):
            return namespace.abort(400, 'ID Product Not Null')
        
        name = content.get("name","NULL")
        detail = content.get("detail","NULL")
        brand = content.get("brand","NULL")
        price = content.get("price","NULL")
        category_id = content.get("category_id","NULL")
        image = content.get("image","NULL")
        size = content.get("size","NULL")
        video = content.get("video","NULL")
        color = content.get("color","NULL")
        quantity = content.get("quantity","NULL")

        cur = con.cursor()
        cur.execute("SELECT id FROM products WHERE id = {};".format(id))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID Product Not Found')
        
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


