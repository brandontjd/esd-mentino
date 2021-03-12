import pika
import json

class Channel:
  def __init__(self, hostname, port, exchangename, exchangetype):
    self.hostname = hostname
    self.port = port
    self.exchangename = exchangename
    self.exchangetype = exchangetype

    self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=hostname, port=port,
            heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
        )
      )
    self.channel = self.connection.channel()

  def set_consume_callback(self, queue, callback):
    self.callback = self.get_wrapped_callback(callback)
    self.channel.basic_consume(
      queue=queue, 
      on_message_callback=self.callback, 
      auto_ack=True
    )
  
  def start_consuming(self):
    return self.channel.start_consuming()

  def basic_publish(self, routing_key, body_dict):
    self.check_setup()
    self.channel.basic_publish(
      exchange=self.exchangename, 
      routing_key=routing_key, 
      body=json.dumps(body_dict), 
      properties=pika.BasicProperties(delivery_mode = 2)
    ) 
    
  def is_connection_open(self):
    try:
        self.connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False

  def check_setup(self):
    if not self.is_connection_open():
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname, port=self.port))
    if self.channel.is_closed:
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchangename, exchange_type=self.exchangetype)

  def get_wrapped_callback(self, callback):
    def wrapped_callback(*args, **kwargs):
      self.check_setup()
      return callback(*args, **kwargs)
    return wrapped_callback