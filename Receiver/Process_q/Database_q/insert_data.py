import MySQLdb as mdb


class InsertData(object):

    def __init__(self, queuedata):
        self.queuedata = queuedata
        con = mdb.connect('localhost', 'root', '', 'api');