from flask import Flask, request
from flask.ext.restful import Resource, Api, reqparse
import MySQLdb as mdb
import MySQLdb.cursors

app = Flask(__name__)
api = Api(app)

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

api.add_resource(DataChecker, '/login/')

if __name__ == '__main__':
    app.run(debug=True)