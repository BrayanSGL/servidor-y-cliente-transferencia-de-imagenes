import socket
import os
import struct


HOST = socket.gethostbyname(socket.gethostname())
IP = socket.gethostbyname(socket.gethostname())
PORT = 65123
DOCUMENTS = '../server/documents/'


class Send():
    def __init__(self, connection, documents: str) -> None:
        self.sck = connection
        self.documents = documents
        self.images = []

    def __send_file(self, url):
        # Obtener el tamaño del archivo a enviar.
        filesize = os.path.getsize(url)
        # Informar primero al servidor la cantidad
        # de bytes que serán enviados.
        self.sck.sendall(struct.pack("<Q", filesize))
        # Enviar el archivo en bloques de 1024 bytes.
        with open(url, "rb") as f:
            while read_bytes := f.read(1024):
                self.sck.sendall(read_bytes)

    def send(self) -> str:
        data = str(self.sck.recv(1024))
        contents = os.listdir(self.documents)
        for fichero in contents:
            if os.path.isfile(os.path.join(self.documents, fichero)) and (fichero.endswith('.jpg')):
                self.images.append(fichero)
        delim = ','
        lista = delim.join(self.images)
        self.sck.send(lista.encode("utf-8"))
        photo = str(self.sck.recv(1024))
        photo = photo.strip("b'")
        print('Archivo a descargar', photo)
        self.__send_file(self.documents+'/'+photo)


class Receive():
    def __init__(self, connection, documents: str) -> None:
        self.sck = connection
        self.documents = documents

    def __size(self, sck: socket.socket) -> int:
        # Esta función se asegura de que se reciban los bytes
        # que indican el tamaño del archivo que será enviado,
        # que es codificado por el cliente vía struct.pack(),
        # función la cual genera una secuencia de bytes que
        # representan el tamaño del archivo.
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        received_bytes = 0
        stream = bytes()
        while received_bytes < expected_bytes:
            chunk = sck.recv(expected_bytes - received_bytes)
            stream += chunk
            received_bytes += len(chunk)
        filesize = struct.unpack(fmt, stream)[0]
        print(filesize)
        return filesize

    def __receive(self, sck: socket.socket, file_name: str):
        # Leer primero del socket la cantidad de
        # bytes que se recibirán del archivo.
        file_size = self.__size(sck)
        # Abrir un nuevo archivo en donde guardar
        # los datos recibidos.
        with open(file_name, "wb") as file:
            received_bytes = 0
            # Recibir los datos del archivo en bloques de
            # 1024 bytes hasta llegar a la cantidad de
            # bytes total informada por el cliente.
            while received_bytes < file_size:
                chunk = sck.recv(1024)
                if chunk:
                    file.write(chunk)
                    received_bytes += len(chunk)

    def receive(self):  # Command text or image
        name = str(self.sck.recv(1024))
        name = name.strip("b'")
        self.sck.send(b'Nombre recibido en el servidor')
        final = (name+'.jpg')
        print('Su archivo se encuentra en la carpeta documents con el nombre de '+final)
        self.__receive(self.sck, (self.documents+'/'+final))
        self.sck.send(b'Archivo recibido en el servidor')
        print('Archivo recibido')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.bind((IP, PORT))
        print('Esperando al cliente en la IP: '+IP+' en el puerto: '+str(PORT))
        sck.listen()
        connection, address = sck.accept()
        while True:
            # ·····Comandos   se debe primero entender que es lo que se quiere hacer
            print(f'Conectado a: {address[0]} en el puerto: {address[1]}')
            data = str(connection.recv(1024))
            data = data.strip("b'")
            connection.send(b'Recibido en el servidor')
            if data == 'Send':
                receive = Receive(connection, DOCUMENTS)
                receive.receive()
            elif data == 'Download':
                send = Send(connection, DOCUMENTS)
                send.send()
            elif data == 'Close':
                connection.close()
                print('Conexión cerrada desde el cliente')
                break


if __name__ == '__main__':
    main()
