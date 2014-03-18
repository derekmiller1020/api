import pika
import json
import time
import datetime
import logging
from Process_q.q_mapping import Mapping


#consumer class. takes in variables from the settings files
class Consumer(object):
    def __init__(self, connection, exchange, host, routing_key, exchange_type):

        #class variables for the below functions
        self.EXCHANGE = exchange
        self.ROUTING_KEY = routing_key
        self.EXCHANGE_TYPE = exchange_type
        self.QUEUE = 'sender'
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = connection

    #Connecting to RabbitMQ
    def connect(self):
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    #Closes rabbitMQ connection
    def close_connection(self):
        self._connection.close()

    #Adds close callback when rabbitmq closes the connection unexpectedly
    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    #Happens when RabbitMQ is closed unexpectedly
    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._connection.add_timeout(5, self.reconnect)

    #used by pika once connection to RabbitMQ has been established
    def on_connection_open(self, unused_connection):
        self.add_on_connection_close_callback()
        self.open_channel()

    #Invoked by the IOLoop timer if the connection is closed
    def reconnect(self):
        self._connection.ioloop.stop()

        if not self._closing:
            self._connection = self.connect()
            self._connection.ioloop.start()

    #Method tells pika to call the on_channel_closed method if loss of channel occurs
    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    #used in case pika or rabbitmq  unexpectedly close
    def on_channel_closed(self, channel, reply_code, reply_text):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    #method invoked when the channel has been opened
    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    #Sets up the RabbitMQ exchange
    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(self.on_exchange_declareok, exchange_name, self.EXCHANGE_TYPE, durable=True)

    #Invoked by Pika when RabbitMQ has finished the Exchange.Declare RPC command
    def on_exchange_declareok(self, unused_frame):
        self.setup_queue(self.QUEUE)

    #Sets up the rabbitmq Queue
    def setup_queue(self, queue_name):
        self._channel.queue_declare(self.on_queue_declareok, queue_name)

    #Invoked when the Queue.Declare RPC call made in setup_queue has completed
    def on_queue_declareok(self, method_frame):
        self._channel.queue_bind(self.on_bindok, self.QUEUE, self.EXCHANGE, self.ROUTING_KEY)

    #Add a callback that will be invoked if RabbitMQ cancels the consumer
    def add_on_cancel_callback(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    #Pika invokes this method when RabbitMq cancels a message
    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    #Acknowledging the message
    def acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    #Where the magic happens. This delivers the message to the appropriate classes to send to the directed user
    def on_message(self, unused_channel, basic_deliver, properties, body):

        #putting the data into a dictionary
        json_acceptable_string = body.replace("'", "\"")
        queuedata = json.loads(json_acceptable_string)

        print "it hit the consumer"

        #Instantiating the mapping class
        try:
            x = Mapping(queuedata['request_type'], queuedata)
        except:
            logging.basicConfig(level=logging.DEBUG, filename='error.log')
            logging.exception("Oops!: ")

        #can be removed. Just datetime stamps
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        print "done at %r" % st

        #Moved this down here.  The message gets dequeued (deleted!) once the ack message is sent.
        #We don't want this to happen until we're sure we're done w/ it.
        #Cool Beans!
        self.acknowledge_message(basic_deliver.delivery_tag)

    def on_cancelok(self, unused_frame):
        self.close_channel()

    #stops consuming rabbitmq messages
    def stop_consuming(self):
        if self._channel:
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    #starts consuming rabbitMQ messages
    def start_consuming(self):
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.QUEUE)

        #Invoked when Queue.bind has been completed
    def on_bindok(self, unused_frame):
        self.start_consuming()

    #Closes the channel with RabbitMQ cleanly
    def close_channel(self):
        self._channel.close()

    #Opens the appropriate channel
    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_open)

    #run the consumer
    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    #stop the consumer
    def stop(self):
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()