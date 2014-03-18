import time
import datetime
from consumer import Consumer
from settings import *

def main():
    #datetime can be removed
    retrieve = Consumer(CONNECTION_URL, EXCHANGE, HOST, ROUTING_KEY, EXCHANGE_TYPE)
    try:
        retrieve.run()
    except KeyboardInterrupt:
        retrieve.stop()

if __name__ == '__main__':
    main()