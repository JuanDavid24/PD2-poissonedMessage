import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.exchange_declare(exchange='DLX',exchange_type='direct')
args = ({'x-dead-letter-exchange': 'DLX'})
channel.queue_declare(queue='cola',arguments=args)
channel.basic_publish(exchange = '',
                      routing_key = 'cola',
                      body = json.dumps((9,0)),
                      properties = pika.BasicProperties(headers= {"x-delivery-attempts": 0})
                      )

connection.close()

