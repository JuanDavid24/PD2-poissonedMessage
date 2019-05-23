import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.queue_declare(queue='cola')

def callback(ch, method, properties, body):
    recibed = json.loads(body)
    print("Recibido: " + str(recibed))
    h = properties.headers

    print(type(h)) #output -> <class 'dict'>
    #print(h['x-delivery-attempts'])    #-> cuando descomento esto la linea de arriba devuelve Nonetype en vez de dict. No puedo acceder a la key


channel.basic_consume(queue='cola',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()