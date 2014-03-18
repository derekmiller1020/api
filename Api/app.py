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

                    if cur.fetchone == 0:
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

api.add_resource(DataChecker, '/login/')

if __name__ == '__main__':
    app.run(debug=True)