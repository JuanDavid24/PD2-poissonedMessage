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

print('\n*Waiting for message to arrive...*')

def callback(ch, method, properties, body):
    recibed = json.loads(body)
    print("\nRecibido: " + str(recibed))
    print("delivery tag: " + str(method.delivery_tag))

    try:
        result = recibed[0] / recibed[1]
        print ("resultado: " + str(result))

    except:
        #print(properties.headers)
        attempts = properties.headers['x-delivery-attempts']
        attempts += 1
        if attempts < 3:
            print("attempts: {at} ".format(at=attempts))

            channel.basic_publish(exchange='',
                                  routing_key='cola2',
                                  body=json.dumps(recibed),
                                  properties=pika.BasicProperties(headers={"x-delivery-attempts": attempts})
                                  )
            print("republished with x-header modified")
            channel.basic_ack(method.delivery_tag)

        else:
            channel.basic_nack(method.delivery_tag, requeue=False)
            print("message {tag} dead-lettered after {at} attempts".format(at= attempts, tag=method.delivery_tag))

channel.basic_consume(queue='cola2',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()