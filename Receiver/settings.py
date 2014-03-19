HOST = 'localhost'
EXCHANGE = 'api'
ROUTING_KEY = 'sender'
QUEUE = 'sender'
EXCHANGE_TYPE = 'topic'
USER = 'guest'
PASS = 'guest'
HOST_PORT = 5672
HEARTBEAT_INTERVAL = 3600
CONNECTION_URL = 'amqp://%s:%s@%s:%d/%%2F?heartbeat_interval=%d' % (USER, PASS, HOST, HOST_PORT, HEARTBEAT_INTERVAL)


