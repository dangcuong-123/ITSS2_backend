from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json

namespace = Namespace('plan', 'Plan Information')

parser_name = reqparse.RequestParser()
parser_name.add_argument('location_name', type=str, help='Location\'s name (eg: ha long)')
@namespace.route('/recommend_transport', methods=['GET'])
class RecommendTransportByName(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Invalid value - Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_name)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        loc_name = request.args.get('location_name', default="NULL") #name = ao
        if(loc_name == "NULL"):
            return namespace.abort(400, 'Invalid value')
        loc_name = loc_name.lower()
        transport_query = cur.execute(f'''select train, car, ship, motorbike from rcm_transport as r
                        where r.location_name like '%{loc_name}%' COLLATE NOCASE;''').fetchall()
        
        if len(transport_query) == 0:
            return namespace.abort(400, 'Not Found')
        else:
            keys = ['train', 'car', 'ship', 'motorbike']
            transport_list = []
            for idx, val in enumerate(transport_query[0]):
                if val == 1:
                    transport_list.append(keys[idx])
        cur.close()
        return {'transport_list':transport_list}


parser_plan = reqparse.RequestParser()
parser_plan.add_argument(
    'location_id', type=int, help='location id (eg: 1)', location='json')
parser_plan.add_argument(
    'hotel_id', type=int, help='hotel id (eg: 1)', location='json')
parser_plan.add_argument(
    'restaurant_id', type=int, help='restaurant id (eg: 1)', location='json')
parser_plan.add_argument(
    'user_id', type=int, help='user id (eg: 1)', location='json')

@namespace.route('/create', methods=['POST'])
class CreatePlan(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_plan, validate=True)

    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        location_id = content.get("location_id", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_id = content.get("restaurant_id", "NULL")
        user_id = content.get("user_id", 'NULL')

        plan = (location_id, hotel_id, restaurant_id, user_id)
        sql = '''INSERT INTO plans (location_id, hotel_id, restaurant_id, user_id) VALUES (?, ?, ?, ?);'''

        cur.execute(sql, plan)
        con.commit()
        cur.close()

        return "create plan successfully"

@namespace.route('/show')
class ShowPlans(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plans_query = cur.execute(
            "SELECT * FROM plans;").fetchall()
        if(len(plans_query) == 0):
            return namespace.abort(400, 'Not Found')
        else:
            plans = []
            for idx, plan_info in enumerate(plans_query):
                plan = {}
                print(plan_info)
                for i, val in enumerate(plan_info):
                    if i==0:
                        plan['plan_id'] = idx
                    elif i==1:
                        loc_query = cur.execute(f"SELECT location_name FROM tourist_destination where tourist_destination.location_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['location_name'] = loc_query[0][0]
                        else:
                            plan['location_name'] = 'None'
                    elif i==2:
                        loc_query = cur.execute(f"SELECT hotel_name FROM hotels where hotels.hotel_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['hotel_name'] = loc_query[0][0]
                        else:
                            plan['hotel_name'] = 'None'
                    elif i==3:
                        loc_query = cur.execute(f"SELECT restaurant_name FROM restaurants where restaurants.restaurant_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['restaurant_name'] = loc_query[0][0]
                        else:
                            plan['restaurant_name'] = 'None'
                    elif i==4:
                        loc_query = cur.execute(f"SELECT name FROM users where users.user_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['user_name'] = loc_query[0][0]
                        else:
                            plan['user_name'] = 'None'
                plans.append(plan)
        cur.close()

        return {'plans': plans}

parser_id = reqparse.RequestParser()
parser_id.add_argument('user_id', type=int, help='User id')
@namespace.route('/get_plans_by_user_id')
class GetPlansByUserId(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        user_id = request.args.get('user_id', default="NULL") #name = ao
        if(user_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        user_query = cur.execute(f'select * from users where users.user_id={user_id};').fetchall()
        if(len(user_query) == 0):
            return namespace.abort(400, 'User Not Exists')
        plans_query = cur.execute(
            f"SELECT * FROM plans where plans.user_id={user_id};").fetchall()

        if(len(plans_query) == 0):
            return namespace.abort(400, 'User Have No Plans')
        else:
            plans = []
            for idx, plan_info in enumerate(plans_query):
                plan = {}
                print(plan_info)
                for i, val in enumerate(plan_info):
                    if i==0:
                        plan['plan_id'] = idx
                    elif i==1:
                        loc_query = cur.execute(f"SELECT location_name FROM tourist_destination where tourist_destination.location_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['location_name'] = loc_query[0][0]
                        else:
                            plan['location_name'] = 'None'
                    elif i==2:
                        loc_query = cur.execute(f"SELECT hotel_name FROM hotels where hotels.hotel_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['hotel_name'] = loc_query[0][0]
                        else:
                            plan['hotel_name'] = 'None'
                    elif i==3:
                        loc_query = cur.execute(f"SELECT restaurant_name FROM restaurants where restaurants.restaurant_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['restaurant_name'] = loc_query[0][0]
                        else:
                            plan['restaurant_name'] = 'None'
                    elif i==4:
                        loc_query = cur.execute(f"SELECT name FROM users where users.user_id={val};").fetchall()
                        if len(loc_query) != 0:
                            plan['user_name'] = loc_query[0][0]
                        else:
                            plan['user_name'] = 'None'
                plans.append(plan)
        cur.close()

        return {'plans': plans}
