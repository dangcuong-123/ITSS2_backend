from flask import request, json
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import re

namespace = Namespace('authenticate', 'Login and Signup')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

parser_login = reqparse.RequestParser()
parser_login.add_argument('email', type=str, help='User\'s email (eg: hieu@gmail.com)', location='json')
parser_login.add_argument('password', type=str, help='User\'s name (eg: hieuhieu)', location='json')
@namespace.route('/login', methods=['POST'])
class Login(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(parser_login, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)

        email = content.get("email", "NULL")
        password = content.get("password", "NULL")
        if(email == "NULL" or password == "NULL"):
            return namespace.abort(400, 'Email Or Password Not Null')
        if not check(email):
            return namespace.abort(400, 'Invalid Email')
        cur = con.cursor()
        cur.execute('''select name, email, password, image_url from users where email = '{}' and password = {};'''.format(
            email, '''\'''' + password + '''\''''))
        # cur.execute(f'''select email, password from users where email='hieu@gmail.com' and password='hieuhieu';''')
        fetchdata = cur.fetchall()
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'Email Or Password Not Found')

        con.commit()
        cur.close()

        return fetchdata


parser_add = reqparse.RequestParser()
parser_add.add_argument('name', type=str, help='User\'s name (eg: vai)', location='json')
parser_add.add_argument('email', type=str, help='User\'s email', location='json')
parser_add.add_argument('password', type=str, help='User\'s password (eg: password)', location='json')
@namespace.route('/signup', methods=['POST'])
class SignUp(Resource):
    @namespace.expect(parser_add, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)
        name = content.get('name', "NULL")
        email = content.get('email', "NULL")
        password = content.get('password', "NULL")

        if not check(email):
            return namespace.abort(400, 'Invalid Email')

        cur = con.cursor()
        cur.execute(
            '''select email, password from users where email = '{}';'''.format(email))
        fetchdata = cur.fetchall()

        if(len(fetchdata) != 0):
            cur.close()
            return namespace.abort(400, 'User exist')
        else:
            cur.execute("INSERT INTO users (name, email, password) VALUES (\"{}\", \"{}\", \"{}\");".format
                        (name, email, password))
        con.commit()
        cur.close()
        return 'Successfully Added User'

parser_edit = reqparse.RequestParser()
parser_edit.add_argument('user_id', type=int, help='User\'s id (eg: 1)', location='json')
parser_edit.add_argument('name', type=str, help='User\'s name (eg: vai)', location='json')
parser_edit.add_argument('email', type=str, help='User\'s email', location='json')
parser_edit.add_argument('password', type=str, help='User\'s password (eg: password)', location='json')
@namespace.route('/edit_profile', methods=['PUT'])
class EditProfile(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Error - ID hotel Not Found - ID hotel Not Null - ID Category Not Found')
    @namespace.response(200, 'Successfully edit')
    @namespace.expect(parser_edit, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        content = json.loads(request.data)
        user_id = content.get('user_id', "NULL")
        name = content.get('name', "NULL")
        email = content.get('email', "NULL")
        password = content.get('password', "NULL")

        if(user_id == "NULL"):
            return namespace.abort(400, 'ID user Not Null')

        if not check(email):
            return namespace.abort(400, 'Invalid Email')

        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE user_id = {};".format(
            user_id))
        fetchdata = cur.fetchall()
        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID User Not Found')

        cols = ['name', 'email', 'password']
        inputs = [name, email, password]
        for i, col in enumerate(cols):
            if(inputs[i] != None):
                cur.execute("UPDATE users SET {} = \"{}\" WHERE user_id = {};".format(
                    col, inputs[i], user_id))

        con.commit()
        cur.close()
        return 'Successfully Added User'

