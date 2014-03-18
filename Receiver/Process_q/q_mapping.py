from Database_q.insert_data import InsertData
from Database_q.retrieve_data import RetrieveData

class Mapping(object):

    def __init__(self, action_type, queuedata):

        self.action_type = action_type
        self.queuedata = queuedata

    def mapping(self):

        action_mapping = {
            'insert': self.insert_data,
            'request': self.request_data
        }

        the_action = action_mapping[self.action_type]()

    def insert_data(self):
        InsertData(self.queuedata)

    def request_data(self):
        RetrieveData(self.queuedata)