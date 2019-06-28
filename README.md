## Actividad Poisson message con RabbitMQ

**1.** Crear container para el server:
```bash 
docker run -d --name rabbitmq-sv rabbitmq
```
**2.** Crear una imagen para el cliente de rabbit:
```bash 
docker build -t rabbitmq-cli-im .
```
#### Problem: 
<b>Muestra la situacion en la cual un dead letter llega a la cola de mensajeria y no es tratada. Para esto: </b> 

**3a.** Correr un container para el consumidor. Estará linkeado al del servidor de Rabbitmq:
```bash 
docker run --name p-receiver -it --rm --link rabbitmq-sv:rb -v $(pwd):/program -w /program rabbitmq-cli-im python3 problem/receiver.py
```

**4a.** Correr un segundo container a partir de esa imagen, el cual estará linkeado al del servidor de Rabbitmq. Desde éste se correrá el programa y enviara un mensaje a la cola:
```bash 
docker run --name p-sender -it --rm --link rabbitmq-sv:rb -v $(pwd):/program -w /program rabbitmq-cli-im python3 problem/sender.py
```
Esto envía un mensaje a la cola el cual. Al haber un error, será reencolado indefinidamente.

#### Solution:
<b>Solución aplicando dead-lettering. Para esto, en terminales independientes:</b>

**3b.** Correr un container para el consumidor:
```bash 
docker run --name s-receiver -it --rm --link rabbitmq-sv:rb -v $(pwd):/program -w /program rabbitmq-cli-im python3 solution/receiver.py
```
**4b.** Crear un container para el módulo que recibe dead letters:
```bash 
docker run --name s-dlreceiver -it --rm --link rabbitmq-sv:rb -v $(pwd):/program -w /program rabbitmq-cli-im python3 solution/DLreceiver.py
```
**5b.** Y finalemnte, el container que enviara el mensaje:
```bash 
docker run --name s-sender -it --rm --link rabbitmq-sv:rb -v $(pwd):/program -w /program rabbitmq-cli-im python3 solution/sender.py
```
Se hará 3 intentos por tratar el mensaje. Al fallar, se enviará a la cola de dead letters.

En la consola de ```s-dlreceive``` se mostrarán los mensajes marcados como dead letter previamente, una vez recibidos. Se indica contenido, fecha, cola original y motivo.

