import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
args = ({'x-dead-letter-exchange': ''})
channel.queue_declare(queue='cola',arguments=args)
channel.basic_publish(exchange = '',
                      routing_key = 'cola',
                      body = json.dumps((7,0)),
                      properties = pika.BasicProperties(headers= {"x-delivery-attempts": 0})
                      )

connection.close()

