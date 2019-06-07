import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-sv'))
channel = connection.channel()
channel.queue_declare(queue='cola')

def callback(ch, method, properties, body):
    received = json.loads(body)
    print("\nReceived: " + str(received))
    print("Delivery tag: " + str(method.delivery_tag))

    try:
        result = received[0] / received[1]
        print ("Resultado: " + str(result))

    except:
        print("Error when processing message. Message re-queued ")
        channel.basic_nack(method.delivery_tag, requeue=True)

channel.basic_consume(queue='cola',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()