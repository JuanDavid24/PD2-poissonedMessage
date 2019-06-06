## Actividad Poissoned message con RabbitMQ

**1.** Crear container para el server :
`docker run --name rabbitmq-sv rabbitmq`

**2.** Crear una imagen para el cliente de rabbit:
`docker build -t rabbitmq-cli-im .`

**3.** Correr un nuevo container a partir de esa imagen, el cual estará linkeado al del servidor de Rabbitmq. Desde éste se correrá el programa que envía mensajes a la cola:
`docker run --name sender -it --link rabbitmq-sv:rb -v $(pwd):/program rabbitmq-cli-im`

**4.** En una segunda terminal, creo el container para el consumidor:
`docker run --name receiver -it --link rabbitmq-sv:rb -v $(pwd):/program rabbitmq-cli-im`

**5.** Dentro de este ultimo container:
`cd program`
y luego:
`python3 problem/receiver.py`

**6.** Despues, en la primer terminal:
`cd program`
y luego:
`python3 problem/sender.py`
