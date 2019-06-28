import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.queue_declare(queue='cola1')
channel.basic_publish(exchange = '',
                      routing_key = 'cola1',
                      body = json.dumps((7,0)),
                      properties = pika.BasicProperties(headers= {"x-delivery-attempts": 0})
                      )
print ("message sent!")
connection.close()

