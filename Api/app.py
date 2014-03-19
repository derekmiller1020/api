from flask import Flask, request
from flask.ext.restful import Resource, Api, reqparse
import MySQLdb as mdb
import MySQLdb.cursors
import uuid
import re

app = Flask(__name__)
api = Api(app)

#This checks the login credentials
class DataChecker(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('password', type=str, location='form')
        self.args = self.parser.parse_args()

    def post(self):
        inspect_data = self.data_inspector()
        return inspect_data

    def data_inspector(self):

        conn = mdb.connect('localhost', 'root', '', 'api', cursorclass=MySQLdb.cursors.DictCursor)
        with conn:

            cur = conn.cursor()
            query = "SELECT * FROM users WHERE username = '%s'" % self.args['username']
            cur.execute(query)
            rows = cur.fetchone()

            if rows == None:
                return {'success': 'False', 'username_message': 'The username was not found'}

            elif self.args['password'] != rows['password']:
                return {'success': 'False', 'password_message': 'The password was incorrect'}

            elif self.args['username'] == rows['username']:
                if self.args['password'] == rows['password']:
                    return {'success': 'True', 'user_id': rows['unique_id']}

            else:
                return {'success': 'False', 'username_message': 'it is over'}

#this is the Registration process
class Registration(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('password', type=str, location='form')
        self.args = self.parser.parse_args()

    def post(self):
        insert_data = self.insert_data()
        return insert_data

    def insert_data(self):

        if re.match("^[A-Za-z0-9_-]*$", self.args['username']):
            if re.match("^[A-Za-z0-9_-]*$", self.args['password']):
                conn = mdb.connect('localhost', 'root', '', 'api', cursorclass=MySQLdb.cursors.DictCursor)
                with conn:
                    cur = conn.cursor()
                    select_query = "SELECT username FROM users WHERE username = '%s'" % self.args['username']
                    cur.execute(select_query)

                    if cur.rowcount == 0:
                        insert_query = "INSERT INTO users (unique_id, username, password) VALUES ('%s', '%s', '%s')" \
                            % (uuid.uuid4(), self.args['username'], self.args['password'])
                        cur.execute(insert_query)

                        return {'success': 'True'}

                    else:
                        return {'success': 'False', 'message': 'That username is already taken'}

            else:
                return {'success': 'False', 'message': 'You have illegal characters in your password'}

        else:
            return {'success': 'False', 'message': 'You have illegal characters in your username'}

class FormInsert(Resource):

    def __init(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('unique_id', type=str, location='form')
        self.parser.add_argument('name', type=str, location='form')
        self.parser.add_argument('food', type=str, location='form')
        self.parser.add_argument('music', type=str, location='form')
        self.parser.add_argument('movie', type=str, location='form')
        self.parser.add_argument('book', type=str, location='form')
        self.parser.add_argument('poem', type=str, location='form')
        self.parser.add_argument('quote', type=str, location='form')
        self.args = self.parser.parse_args()

    def post(self):
        insert_data = self.insert_data()
        return insert_data

    def insert_data(self):

        conn = mdb.connect('localhost', 'root', 'password', 'api', cursorclass=MySQLdb.cursors.DictCursor)
        with conn:
            cur = conn.cursor()
            select_query = "SELECT full_name, food, music, movie, book, poem, quote FROM form WHERE unique_id = '%s'" \
                           % self.args['unique_id']
            cur.execute(select_query)

            if cur.rowcount == 0:
                insert_query = """
                               INSERT INTO form (unique_id, full_name, food, music, movie, book, poem, quote) VALUES
                               ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                               """ % (self.args['unique_id'], self.args['name'], self.args['food'], self.args['music'],
                               self.args['movie'], self.args['book'], self.args['poem'], self.args['quote'])
                cur.execute(insert_query)
                return {'success': 'True'}
            else:
                update_query = """
                               UPDATE form SET full_name='%ss', food='%s', music='%s', movie='%s', book='%s', poem='%s',
                                quote='%s' WHERE unique_id = '%s')
                               """ % (self.args['name'], self.args['food'], self.args['music'], self.args['movie'],
                                      self.args['book'], self.args['poem'], self.args['quote'], self.args['unique_id'])
                cur.execute(update_query)
                return {'success': 'True'}


api.add_resource(DataChecker, '/login/')
api.add_resource(Registration, '/register/')
api.add_resource(FormInsert, '/insertform/')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.56.101')