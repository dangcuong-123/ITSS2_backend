from os import name
from flask import request, json
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import re

namespace = Namespace('authen', 'Login and Signup')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

parser_login = reqparse.RequestParser()
parser_login.add_argument('email', type=str, help='user\'s email (eg: hieu@gmail.com)', location='json')
parser_login.add_argument('password', type=str, help='Product\'s name (eg: quan dai)', location='json')
@namespace.route('/login', methods=['POST'])
class Login(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(parser_login, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)

        email = content.get("email","NULL")
        password = content.get("password","NULL")
        if(email == "NULL" or password == "NULL"):
            return namespace.abort(400, 'Email Or Password Not Null')
        if not check(email):
            return namespace.abort(400, 'Invalid Email')
        cur = con.cursor()
        cur.execute('''select email, password from users where email = '{}' and password = {};'''.format(email, '''\'''' + password + '''\''''))
        # cur.execute(f'''select email, password from users where email='hieu@gmail.com' and password='hieuhieu';''')
        fetchdata = cur.fetchall()
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'Email Or Password Not Found')
        
        con.commit()
        cur.close()

        return 'Successfully Login'

parser_add = reqparse.RequestParser()
parser_add.add_argument('name', type=str, help='User\'s name (eg: vai)', location='form')
parser_add.add_argument('email', type=str, help='User\'s email', location='form')
parser_add.add_argument('password', type=str, help='User\'s password (eg: password)', location='form')
parser_add.add_argument('image_url', type=str, help='User\'s image url (eg: sfdfsdf)', location='form')
@namespace.route('/signup', methods=['PUT'])
class SignUp(Resource):
    
    @namespace.expect(parser_add, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        name = request.form.get('name', default="NULL")
        email = request.form.get('email', default="NULL")
        password = request.form.get('password', default="NULL")
        image_url = request.form.get('image_url', default="NULL")
        
        if not check(email):
            return namespace.abort(400, 'Invalid Email')
            
        cur = con.cursor()
        cur.execute('''select email, password from users where email = '{}';'''.format(email))
        fetchdata = cur.fetchall()
        
        if(len(fetchdata) != 0):
            cur.close()
            return namespace.abort(400, 'User exist')
        else:
            cur.execute("INSERT INTO users (name, email, password, image_url) VALUES (\"{}\", \"{}\", \"{}\", \"{}\");".format
                        (name, email, password, image_url))
        con.commit()
        cur.close()
        return 'Successfully Added User'

