import MySQLdb as mdb
import MySQLdb.cursors
import uuid
import re

class MysqlStuff(object):

    def __init__(self):
        self.conn = mdb.connect('localhost', 'root', 'password', 'api', cursorclass=MySQLdb.cursors.DictCursor)
        self.cur = self.conn.cursor()

    def login_check(self, username, password):

        with self.conn:

            query = "SELECT * FROM users WHERE username = '%s'" % username
            self.cur.execute(query)
            rows = self.cur.fetchone()

            if rows == None:
                return {'success': 'False', 'username_message': 'The username was not found'}

            elif password != rows['password']:
                return {'success': 'False', 'password_message': 'The password was incorrect'}

            elif username == rows['username']:
                if password == rows['password']:
                    return {'success': 'True', 'user_id': rows['unique_id']}

            else:
                return {'success': 'False', 'username_message': 'What did you do?'}

    def the_registration(self, username, password):

        if re.match("^[A-Za-z0-9_-]*$", username):
            if re.match("^[A-Za-z0-9_-]*$", password):

                with self.conn:
                    select_query = "SELECT username FROM users WHERE username = '%s'" % username
                    self.cur.execute(select_query)

                    if self.cur.rowcount == 0:
                        insert_query = "INSERT INTO users (unique_id, username, password) VALUES ('%s', '%s', '%s')" \
                            % (uuid.uuid4(), username, password)
                        self.cur.execute(insert_query)

                        return {'success': 'True'}

                    else:
                        return {'success': 'False', 'message': 'That username is already taken'}

            else:
                return {'success': 'False', 'message': 'You have illegal characters in your password'}

        else:
            return {'success': 'False', 'message': 'You have illegal characters in your username'}

    def insert_data(self, args):

        with self.conn:
            select_query = "SELECT full_name, food, music, movie, book, poem, quote FROM form WHERE unique_id = '%s'" \
                           % args['unique_id']
            self.cur.execute(select_query)

            if self.cur.rowcount == 0:
                insert_query = """
                               INSERT INTO form (unique_id, full_name, food, music, movie, book, poem, quote) VALUES
                               ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                               """ % (args['unique_id'], args['name'], args['food'], args['music'],
                               args['movie'], args['book'], args['poem'], args['quote'])
                self.cur.execute(insert_query)

                return {'success': 'True'}

            else:
                update_query = """
                               UPDATE form SET full_name='%s', food='%s', music='%s', movie='%s', book='%s', poem='%s',
                                quote='%s' WHERE unique_id = '%s'
                               """ % (args['name'], args['food'], args['music'], args['movie'],
                                      args['book'], args['poem'], args['quote'], args['unique_id'])
                self.cur.execute(update_query)

                return {'success': 'True'}

    def retrieve_data(self, unique_id):

        with self.conn:

            select_query = "SELECT full_name, food, music, movie, book, poem, quote FROM form WHERE unique_id = '%s'" \
                           % unique_id
            self.cur.execute(select_query)
            if self.cur.rowcount == 0:
                return {'message': 'There is nothing here'}
            else:
                rows = self.cur.fetchone()

        return rows

    def retrieve_users(self):

        with self.conn:
            query = "SELECT username, unique_id FROM users"
            self.cur.execute(query)

            if self.cur.rowcount == 0:
                return {'message': 'There are no users sorry'}
            else:
                rows = self.cur.fetchall()

        return rows