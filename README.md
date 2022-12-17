# Proyecto de servidor y cliente de transferencia de imágenes
Este proyecto consiste en un servidor y un cliente que permiten realizar la transferencia de imágenes entre ambos. El servidor se encarga de almacenar las imágenes enviadas por el cliente y de enviar una lista de imágenes disponibles al cliente para su descarga. El cliente, por su parte, puede elegir una de las imágenes de la lista para descargarla o puede enviar una imagen al servidor para que este la almacene.

## Requisitos
Para utilizar este proyecto es necesario contar con Python 3.10 o superior instalado en el sistema.

## Ejecución
Para ejecutar el servidor, se debe ejecutar el siguiente comando en la consola:
```
python server.py
```
Para ejecutar el cliente, se debe ejecutar el siguiente comando en la consola:
```
python client.py
```
Una vez ejecutados ambos programas, el cliente podrá enviar imágenes al servidor y descargar imágenes del servidor.

## Funcionamiento
El servidor y el cliente se comunican utilizando la biblioteca socket de Python. El servidor establece una conexión en el host y puerto especificados en las variables HOST y PORT, respectivamente, y espera a que el cliente se conecte.

Una vez conectado el cliente, este puede elegir entre enviar una imagen al servidor o descargar una imagen del servidor. Si elige enviar una imagen, el servidor recibe la imagen y la almacena en la carpeta "documents". Si elige descargar una imagen, el servidor envía una lista de las imágenes disponibles en la carpeta "documents" y el cliente elige cuál de ellas desea descargar.

## Autores
- Brayan Snader Galeano Lara ([brayangaleanolara](https://github.com/brayangaleanolara))
- Paula Marcela Aragonés Murcia ([paulaa2209](https://github.com/paulaa2209))

## Licencia
Este proyecto está licenciado bajo la licencia MIT. Para más información, consulte el archivo LICENSE.
