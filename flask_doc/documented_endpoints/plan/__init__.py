from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json

namespace = Namespace('plan', 'Plan Information')

parser_name = reqparse.RequestParser()
parser_name.add_argument('location_name', type=str, help='Location\'s name (eg: ha long)')
@namespace.route('/recommend_transport_by_location_name', methods=['GET'])
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
        transport_id_query = cur.execute(f'''select * from tourist_destination as r
                        where r.location_name like '%{loc_name}%' COLLATE NOCASE;''').fetchall()      
        if len(transport_id_query) == 0:
            return namespace.abort(400, 'Not Found')
        else:
            transport_id_query = transport_id_query[0][5]
            transport_query = cur.execute(
            "SELECT * FROM rcm_transport WHERE rcm_transport_id={};".format(transport_id_query)).fetchall()
            keys = ['train', 'car', 'ship', 'motorbike']
            transport_list = []
            for idx, val in enumerate(transport_query[0]):
                if idx > 0:
                    if val == 1:
                        transport_list.append(keys[idx-1])
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
        plan_query = cur.execute(f'''select * from plans as r
                        where r.location_id = {location_id} and r.hotel_id = {hotel_id} and r.restaurant_id = {restaurant_id};''').fetchall()
        if len(plan_query) == 0:
            plan = (location_id, hotel_id, restaurant_id)
            sql = '''INSERT INTO plans (location_id, hotel_id, restaurant_id) VALUES (?, ?, ?);'''
            cur.execute(sql, plan)
            con.commit()
            plan_id = cur.execute(f'''select * from plans order by plan_id desc limit 1;''').fetchall()[0][0]
            cur.execute(f'''INSERT INTO plans_vs_users (plan_id, user_id) VALUES ({plan_id},{user_id});''')
            con.commit()
        else:
            plan_id = plan_query[0][0]
            cur.execute(f'''INSERT INTO plans_vs_users (plan_id, user_id) VALUES ({plan_id},{user_id});''')
            con.commit()
        cur.close()

        return "create plan successfully"


parser_plan = reqparse.RequestParser()
parser_plan.add_argument(
    'location_id', type=int, help='location id (eg: 1)', location='json')
parser_plan.add_argument(
    'hotel_id', type=int, help='hotel id (eg: 1)', location='json')
parser_plan.add_argument(
    'restaurant_id', type=int, help='restaurant id (eg: 1)', location='json')
parser_plan.add_argument(
    'plans_vs_users_id', type=int, help='plans_vs_users_id id (eg: 1)', location='json')

parser_plan.add_argument(
    'user_id', type=int, help='users id (eg: 1)', location='json')

@namespace.route('/edit', methods=['PUT'])
class EditPlan(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_plan, validate=True)

    def put(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        location_id = content.get("location_id", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_id = content.get("restaurant_id", "NULL")
        user_id = content.get("user_id", 'NULL')
        plans_vs_users_id = content.get("plans_vs_users_id", 'NULL')

        plan_query = cur.execute(f'''select * from plans as r
                        where r.location_id = {location_id} and r.hotel_id = {hotel_id} and r.restaurant_id = {restaurant_id};''').fetchall()
        
        if len(plan_query) == 0:
            plan = (location_id, hotel_id, restaurant_id)
            sql = '''INSERT INTO plans (location_id, hotel_id, restaurant_id) VALUES (?, ?, ?);'''
            cur.execute(sql, plan)
            con.commit()
            plan_id = cur.execute(f'''select * from plans order by plan_id desc limit 1;''').fetchall()[0][0]
            cur.execute(f'''UPDATE plans_vs_users SET plan_id={plan_id}, user_id={user_id} WHERE id={plans_vs_users_id};''')
            con.commit()
        else:
            plan_id = plan_query[0][0]
            cur.execute(f'''UPDATE plans_vs_users SET plan_id={plan_id}, user_id={user_id} WHERE id={plans_vs_users_id};''')
            con.commit()
        cur.close()

        return "Edit plan successfully"

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='plans_vs_users_id\'s id (eg: 123)')
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
            "SELECT * FROM plans_vs_users WHERE id = {};".format(id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID location not found')

        cur.execute(
            "DELETE FROM plans_vs_users WHERE id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Plans'

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
                        plan['plan_id'] = val
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
            f"SELECT * FROM plans_vs_users where plans_vs_users.user_id={user_id};").fetchall()
        if(len(plans_query) == 0):
            return namespace.abort(400, 'User Have No Plans')
        else:
            list_plans = [[val for i, val in enumerate(pl) if i==1][0] for pl in plans_query]
            list_plans_vs_users = [[val for i, val in enumerate(pl) if i==0][0] for pl in plans_query]
            plans = []
            for idx, pl_id in enumerate(list_plans):
                plan = {}
                plan['plans_vs_users_id'] = int(list_plans_vs_users[idx])
                plan['username'] = user_query[0][1]
                pl_query = cur.execute(
            f"SELECT * FROM plans where plans.plan_id={pl_id};").fetchall()[0]
                for i, val in enumerate(pl_query):
                    if i==1:
                        plan['plan_id'] = pl_id
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
                
                plans.append(plan)
        
        cur.close()
        return {'plans': plans}

parser_id = reqparse.RequestParser()
parser_id.add_argument('plan_id', type=int, help='User id')
@namespace.route('/get_comments_by_plan_id')
class GetCommentByPlan(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_id) 
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plan_id = request.args.get('plan_id', default="NULL") #name = ao
        if(plan_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(f'select * from comments where comments.plan_id={plan_id} order by comment_time desc;').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Plan Not Exists')
        comments = []
        for idx, cmt in enumerate(comment_query):
            comment = {}
            user_name = cur.execute(f'select * from users where users.user_id={cmt[1]};').fetchall()[0][1]
            comment['user_name'] = user_name
            comment['comment_content'] = cmt[2]
            comment['comment_time'] = cmt[3]
            comment['star_number'] = cmt[5]
            comments.append(comment)
        
        cur.close()

        return {'comments': comments}


parser_id = reqparse.RequestParser()
parser_id.add_argument('plan_id', type=int, help='User id')
@namespace.route('/get_avg_star_by_plan_id')
class GetAVGStarByPlan(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')

    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plan_id = request.args.get('plan_id', default="NULL") #name = ao
        if(plan_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(f'select * from comments where comments.plan_id={plan_id};').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Plan Not Exists')
        else:
            stars = [int(comment[5]) for comment in comment_query]
            if len(stars) == 0:
                return {'avg_star': 0}
            else:
                return {'avg_star':sum(stars)/len(stars)}