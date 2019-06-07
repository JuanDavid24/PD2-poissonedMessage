import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.queue_declare(queue='cola')
channel.basic_publish(exchange = '',
                      routing_key = 'cola',
                      body = json.dumps((7,0)),
                      properties = pika.BasicProperties(headers= {"x-delivery-attempts": 0})
                      )

connection.close()

