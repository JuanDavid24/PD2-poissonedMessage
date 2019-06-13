import pika
import json

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.exchange_declare(exchange='DLX',exchange_type='direct')
channel.queue_declare(queue='poissonQueue')
channel.queue_bind(exchange='DLX',
                   routing_key='cola',
                   queue='poissonQueue')

print('\n*Waiting for dead leteters to arrive...*')

def callback(ch, method, properties, body):
    recibed = json.loads(body)
    dHeader = properties.headers['x-death'][0]

    print("\nRecibed: {r} "
          "\ndelivery tag: {t}\n"
          "\tDead-lettered from queue: {q},\n "
          "\tat {d}, \n "
          "\treason: {rs}.".format(r=recibed, t=method.delivery_tag, q=dHeader['queue'],
                                   d=str(dHeader['time']), rs=dHeader['reason']))
    channel.basic_ack(method.delivery_tag)
    print('\n*Waiting for more dead leteters to arrive...*')

channel.basic_consume(queue='poissonQueue',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()