import MySQLdb as mdb
import MySQLdb.cursors


class RetrieveData(object):

    def __init__(self, queuedata):
        self.queuedata = queuedata
        self.data_type = queuedata['data_type']
        self.data = queuedata['data']
        self.conn = mdb.connect('localhost', 'root', '', 'api')

    def mapping(self):

        retrieve_mapping = {
            'user_info': self.user_info,
            'user_data': self.user_data
        }

        map_action = retrieve_mapping[self.data_type]()

    def user_info(self):
        pass

    def user_data(self):
        pass
