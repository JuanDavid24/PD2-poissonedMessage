import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()

channel.queue_declare(queue='cola')
props = pika.BasicProperties(headers= {'x-delivery-attempts': 0})
channel.basic_publish(exchange = '',
                      routing_key = 'cola',
                      body = json.dumps((6,0)),
                      properties = props
                      )

connection.close()

