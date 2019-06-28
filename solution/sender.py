import pika
import json

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.exchange_declare(exchange='DLX',exchange_type='direct')
args = ({'x-dead-letter-exchange': 'DLX'})
channel.queue_declare(queue='cola2',arguments=args)

channel.queue_declare(queue='poissonQueue')
channel.queue_bind(queue='poissonQueue', exchange='DLX')


channel.basic_publish(exchange = '',
                      routing_key = 'cola2',
                      body = json.dumps((8,0)),
                      properties = pika.BasicProperties(headers= {"x-delivery-attempts": 0})
                      )
print('*Message sent!*\n')
connection.close()

