from flask import Flask, request
from flask.ext.restful import Resource, Api, reqparse

from mysql_stuff import MysqlStuff

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
        draw_class = MysqlStuff()
        inspect_data = draw_class.login_check(self.args['username'], self.args['password'])
        return inspect_data

#this is the Registration process
class Registration(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('password', type=str, location='form')
        self.args = self.parser.parse_args()

    def post(self):
        data_class = MysqlStuff()
        insert_data = data_class.the_registration(self.args['username'], self.args['password'])
        return insert_data


class FormInsert(Resource):

    def __init__(self):

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
        data_class = MysqlStuff()
        insert_data = data_class.insert_data(self.args)
        return insert_data


class PullForm(Resource):

    def get(self, unique_id):
        data_class = MysqlStuff()
        the_info = data_class.retrieve_data(unique_id)

        return the_info

class RetrieveUsers(Resource):

    def get(self):
        data_class = MysqlStuff()
        the_info = data_class.retrieve_users()

        return the_info

api.add_resource(RetrieveUsers, '/users/')
api.add_resource(DataChecker, '/login/')
api.add_resource(Registration, '/register/')
api.add_resource(FormInsert, '/insertform/')
api.add_resource(PullForm, '/pullform/<string:unique_id>')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')