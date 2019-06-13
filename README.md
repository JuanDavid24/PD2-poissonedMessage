## Actividad Poisson message con RabbitMQ

**1.** Crear container para el server:
`docker run --name rabbitmq-sv rabbitmq`
Luego, correrlo:
`docker start rabbitmq-sv`

**2.** Crear una imagen para el cliente de rabbit:
`docker build -t rabbitmq-cli-im .`

**3.** Correr un nuevo container a partir de esa imagen, el cual estará linkeado al del servidor de Rabbitmq. Desde éste se correrá el programa que envía mensajes a la cola:
`docker run --name sender -it --link rabbitmq-sv:rb -v $(pwd):/program rabbitmq-cli-im`

**4.** En una segunda terminal, creo el container para el consumidor:
`docker run --name receiver -it --link rabbitmq-sv:rb -v $(pwd):/program rabbitmq-cli-im`

**5.** En una tercera terminal, creamos un container para el módulo que recibe dead letters:
`docker run --name DLreceiver -it --link rabbitmq-sv:rb -v $(pwd):/program rabbitmq-cli-im`

<h5> A-Problema en cuestión, ocasionado por un poisson message sin tratar: </h5>

**A1.** Dentro del container **receiver**:
`cd program`
y luego:
`python3 problem/receiver.py`

**A2.** Por último, en el container **sender**:
`cd program`
y luego:
`python3 problem/sender.py`

Esto envía un mensaje a la cola el cual. Al haber un error, será reencolado indefinidamente.

<h5> B-Solución aplicando dead-lettering: </h5>

**B1.** Dentro del container **receiver** (ya situado en `program`):

`python3 solution/receiver.py`

**B2.** En el container **DLreceiver**:
`cd program`
y luego:
`python3 solution/DLreceiver.py`

**B3.** En el container **sender** (ya situado en `program`):
`python3 solution/sender.py`

Se hará 3 intentos por tratar el mensaje. Al fallar, se enviará a la cola de dead letters.

En la consola de **DLreceiver** se mostrarán los mensajes marcados como dead letter previamente, una vez recibidos. Se indica contenido, fecha, cola original y motivo.