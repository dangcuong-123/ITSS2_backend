from flask import request
from flask_restx import Namespace, Resource, reqparse
import sqlite3
import json
import datetime

namespace = Namespace('comment', 'Comment Information')


parser_plan = reqparse.RequestParser()

parser_plan.add_argument(
    'hotel_id', type=int, help='hotel id (eg: 1)', location='json')
parser_plan.add_argument(
    'restaurant_id', type=int, help='Restaurant id (eg: 1)', location='json')
parser_plan.add_argument(
    'comment_content', type=str, help='comment content (eg: dep qua)', location='json')
parser_plan.add_argument(
    'username', type=str, help='username (eg: admin)', location='json')
parser_plan.add_argument(
    'star_number', type=int, help='star number (eg: 1)', location='json')


@namespace.route('/create', methods=['POST'])
class CreateComments(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_plan, validate=True)
    def post(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        username = content.get("username", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_id = content.get("restaurant_id", "NULL")
        star_number = content.get("star_number", "NULL")
        comment_content = content.get("comment_content", 'NULL')
        # print("🚀 ~ file: __init__.py:41 ~ user_query", username)
        user_query = cur.execute(
            f'''select * from users where name = "{username}"''').fetchall()
        # print("🚀 ~ file: __init__.py:42 ~ user_query", user_query[0][0])
        user_id = user_query[0][0]
        if hotel_id != "NULL":
            hotel_query = cur.execute(f'''select * from hotels as r
                        where r.hotel_id = {hotel_id};''').fetchall()
            if len(hotel_query) == 0:
                cur.close()
                return namespace.abort(400, 'ID hotel not found')
        if restaurant_id != "NULL":
            restaurant_query = cur.execute(f'''select * from restaurants as r
                        where r.restaurant_id = {restaurant_id};''').fetchall()
            if len(restaurant_query) == 0:
                cur.close()
                return namespace.abort(400, 'ID restaurant not found')
        if len(user_query) == 0:
            cur.close()
            return namespace.abort(400, 'User not found')
        else:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            if hotel_id != "NULL":
                cmt = (user_id, comment_content,
                       current_time, hotel_id, star_number)
                sql = '''INSERT INTO comments (user_id, comment_content, comment_time, hotel_id, star_number) VALUES (?, ?, ?, ?, ?);'''
                cur.execute(sql, cmt)
            else:
                cmt = (user_id, comment_content, current_time,
                       restaurant_id, star_number)
                sql = '''INSERT INTO comments (user_id, comment_content, comment_time, restaurant_id, star_number) VALUES (?, ?, ?, ?, ?);'''
                cur.execute(sql, cmt)

            con.commit()
        cur.close()

        return "create comment successfully"


parser_plan = reqparse.RequestParser()
parser_plan.add_argument(
    'comment_id', type=int, help='Comment id (eg: 1)', location='json')
parser_plan.add_argument(
    'hotel_id', type=int, help='hotel id (eg: 1)', location='json')
parser_plan.add_argument(
    'restaurant_id', type=int, help='Restaurant id (eg: 1)', location='json')
parser_plan.add_argument(
    'comment_content', type=str, help='comment content (eg: dep qua)', location='json')
parser_plan.add_argument(
    'user_id', type=int, help='user id (eg: 1)', location='json')
parser_plan.add_argument(
    'star_number', type=int, help='star number (eg: 1)', location='json')


@namespace.route('/edit', methods=['PUT'])
class EditComment(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(404, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_plan, validate=True)
    def put(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        content = json.loads(request.data)
        comment_id = content.get("comment_id", "NULL")
        user_id = content.get("user_id", "NULL")
        hotel_id = content.get("hotel_id", "NULL")
        restaurant_id = content.get("restaurant_id", "NULL")
        star_number = content.get("star_number", "NULL")
        comment_content = content.get("comment_content", 'NULL')
        comment_query = cur.execute(f'''select * from comments as r
                        where r.comment_id = {comment_id};''').fetchall()
        if len(comment_query) == 0:
            cur.close()
            return namespace.abort(400, 'ID comment not found')
        user_query = cur.execute(f'''select * from users as r
                        where r.user_id = {user_id};''').fetchall()
        if len(user_query) == 0:
            cur.close()
            return namespace.abort(400, 'ID user not found')
        if hotel_id != "NULL":
            hotel_query = cur.execute(f'''select * from hotels as r
                        where r.hotel_id = {hotel_id};''').fetchall()
            if len(hotel_query) == 0:
                cur.close()
                return namespace.abort(400, 'ID hotel not found')
        if restaurant_id != "NULL":
            restaurant_query = cur.execute(f'''select * from restaurants as r
                        where r.restaurant_id = {restaurant_id};''').fetchall()
            if len(restaurant_query) == 0:
                cur.close()
                return namespace.abort(400, 'ID restaurant not found')

        else:
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            # restaurant_id = None
            if hotel_id != "NULL":
                cmt = (user_id, comment_content, current_time,
                       hotel_id, star_number, comment_id)
                sql = '''UPDATE comments SET user_id= ?, comment_content= ?, comment_time= ?, hotel_id= ?, star_number= ? where comment_id=?;'''
                cur.execute(sql, cmt)
            else:
                cmt = (user_id, comment_content, current_time,
                       restaurant_id, star_number, comment_id)
                sql = '''UPDATE comments SET user_id= ?, comment_content= ?, comment_time= ?, restaurant_id= ?, star_number= ? where comment_id=?;'''
                cur.execute(sql, cmt)

            con.commit()
        cur.close()

        return "Update comment successfully"


parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, help='Comment\'s id (eg: 123)')


@namespace.route('/delete', methods=['DELETE'])
class DeleteComment(Resource):
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
            "SELECT * FROM comments WHERE comment_id = {};".format(id))
        fetchdata = cur.fetchall()

        if(len(fetchdata) == 0):
            cur.close()
            return namespace.abort(400, 'ID location not found')

        cur.execute(
            "DELETE FROM comments WHERE comment_id={};".format(id))
        con.commit()

        cur.close()
        return 'Successfully Delete Comment'


@namespace.route('/show')
class ShowComment(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plans_query = cur.execute(
            "SELECT * FROM comments;").fetchall()
        if(len(plans_query) == 0):
            return namespace.abort(400, 'Not Found')

        cur.close()

        return {'comments': plans_query}


parser_id = reqparse.RequestParser()
parser_id.add_argument('hotel_id', type=int, help='Hotel id')


@namespace.route('/get_comments_by_hotel_id')
class GetCommentByHotel(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        hotel_id = request.args.get('hotel_id', default="NULL")  # name = ao
        if(hotel_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(
            f'select * from comments where comments.hotel_id={hotel_id} order by comment_time desc;').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Hotel Not Exists')
        comments = []
        for idx, cmt in enumerate(comment_query):
            comment = {}
            comment['comment_id'] = cmt[0]
            user_name = cur.execute(
                f'select * from users where users.user_id={cmt[1]};').fetchall()[0][1]
            comment['user_name'] = user_name
            comment['comment_content'] = cmt[2]
            comment['comment_time'] = cmt[3]
            comment['star_number'] = cmt[6]
            comments.append(comment)

        cur.close()

        return {'comments': comments}


parser_id = reqparse.RequestParser()
parser_id.add_argument('hotel_id', type=int, help='Restaurant id')


@namespace.route('/get_comments_by_restaurant_id')
class GetCommentByRestaurant(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        hotel_id = request.args.get('hotel_id', default="NULL")  # name = ao
        if(hotel_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(
            f'select * from comments where comments.restaurant_id={hotel_id} order by comment_time desc;').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Hotel Not Exists')
        comments = []
        for idx, cmt in enumerate(comment_query):
            comment = {}
            comment['comment_id'] = cmt[0]
            user_name = cur.execute(
                f'select * from users where users.user_id={cmt[1]};').fetchall()[0][1]
            comment['user_name'] = user_name
            comment['comment_content'] = cmt[2]
            comment['comment_time'] = cmt[3]
            comment['star_number'] = cmt[6]
            comments.append(comment)

        cur.close()

        return {'comments': comments}


parser_id = reqparse.RequestParser()
parser_id.add_argument('plan_id', type=int, help='Hotel id')


@namespace.route('/get_avg_star_by_hotel_id')
class GetAVGStarByHotel(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plan_id = request.args.get('plan_id', default="NULL")  # name = ao
        if(plan_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(
            f'select * from comments where comments.hotel_id={plan_id};').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Plan Not Exists')
        else:
            stars = [int(comment[6]) for comment in comment_query]
            if len(stars) == 0:
                return {'avg_star': 0}
            else:
                return {'avg_star': sum(stars)/len(stars)}


parser_id = reqparse.RequestParser()
parser_id.add_argument('plan_id', type=int, help='Restaurant id')


@namespace.route('/get_avg_star_by_restaurant_id')
class GetAVGStarByRestaurant(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.response(400, 'Not Found')
    @namespace.response(200, 'Success')
    @namespace.expect(parser_id)
    def get(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        plan_id = request.args.get('plan_id', default="NULL")  # name = ao
        if(plan_id == "NULL"):
            return namespace.abort(400, 'Invalid value')
        comment_query = cur.execute(
            f'select * from comments where comments.restaurant_id={plan_id};').fetchall()
        if(len(comment_query) == 0):
            return namespace.abort(400, 'Plan Not Exists')
        else:
            stars = [int(comment[6]) for comment in comment_query]
            if len(stars) == 0:
                return {'avg_star': 0}
            else:
                return {'avg_star': sum(stars)/len(stars)}
