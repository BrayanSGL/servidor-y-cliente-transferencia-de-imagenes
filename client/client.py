import socket
import os
import struct

# ---------------CLIENT-------------

# .....Constans.....
HOST = '192.168.1.64'
PORT = 65123
DOCUMENTS = '../client/documents/'


class Comammad():
    def __init__(self, sck: socket.socket, menu: str, host, port) -> None:
        self.menu = menu
        self.sck = sck
        self.host = host
        self.port = port

    def send_command(self):
        #self.sck.connect((self.host, self.port))

        self.sck.send(self.menu.encode("utf-8"))
        data = self.sck.recv(1024)

        print('\n --------------------')
        print(data.decode("utf-8"))
        print(' -------------------- \n')


class Download():
    def __init__(self, sck: socket.socket, documents: str) -> None:
        self.sck = sck
        self.images = []
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

    def download(self) -> str:
        self.sck.send(b'Download')
        raw_list = str(self.sck.recv(1024))
        raw_list = raw_list.strip("b'")
        self.images = raw_list.split(',')

        os.system('cls')

        print('--------LISTA DE IMÁGENES EN EL SERVER--------\n')
        for i in range(len(self.images)):
            print(f'{i+1} | {self.images[i]}')
        print('\n---------------------------------------------')

        while True:
            selected = input(
                '\n Seleccione una opción (Documento a descargar) > ')
            if selected.isnumeric() and int(selected) > 0 and int(selected) <= len(self.images):
                selected = int(selected)
                break

        self.sck.send(self.images[selected-1].encode("utf-8"))

        self.__receive(self.sck, self.documents+self.images[selected-1])
        #self.sck.send(b'Archivo recibido en el cliente')
        print('Archivo recibido')
        return 'Home'

        '''print('\n --------------------')
        print(repr(raw_list))
        print(' -------------------- \n')'''


class Home():
    def __init__(self) -> None:
        self.is_running = True
        self.OPTIONS = [
            {'number': 1, 'text': 'ENVIAR FOTO', 'command': 'Send'},
            {'number': 2, 'text': 'DESCARGAR FOTO', 'command': 'Download'},
            {'number': 3, 'text': 'CERRAR CONEXIÓN', 'command': 'Close'}
        ]

    def __show_menu(self):
        print(' --------------------------------------------- \n')
        for i in range(len(self.OPTIONS)):
            print(self.OPTIONS[i].get('number'),
                  '|', self.OPTIONS[i].get('text'))
        print('\n --------------------------------------------- ')

    def show_screen(self) -> str:
        while self.is_running:
            os.system('cls')
            self.__show_menu()
            option = input('\n Seleccione una opcion  > ')
            if option.isnumeric() and int(option) > 0 and int(option) <= len(self.OPTIONS):
                return self.OPTIONS[int(option)-1].get('command')


class Send():
    def __init__(self, sck: socket.socket, documents_url: str, name_file: str) -> None:
        self.is_running = True
        self.sck = sck
        self.documents_url = documents_url
        self.images = []
        self.name_file = name_file

    def __show_files(self):
        print('------------LISTA DE IMÁGENES----------------\n')
        for i in range(len(self.images)):
            print(f'{i+1} | {self.images[i]}')
        print('\n---------------------------------------------')

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

        data = self.sck.recv(1024)

        print('\n --------------------')
        print(repr(data))
        print(' -------------------- \n')

    def __send_name(self, name: str):
        self.sck.send(name.encode("utf-8"))
        data = self.sck.recv(1024)

        print('\n --------------------')
        print(repr(data))
        print(' -------------------- \n')

    def send_file(self) -> str:
        contents = os.listdir(self.documents_url)
        for fichero in contents:
            if os.path.isfile(os.path.join(self.documents_url, fichero)) and (fichero.endswith('.jpg')):
                self.images.append(fichero)

        while self.is_running:
            os.system('cls')
            self.__show_files()
            selected = input(
                '\n Seleccione una opción (Documento a enviar) > ')
            if selected.isnumeric() and int(selected) > 0 and int(selected) <= len(self.images):
                selected = int(selected)
                break

        self.name_file = input(
            f'\n Ingrese el nombre con el que desea enviar {self.images[selected-1]} > ')

        self.__send_name(self.name_file)
        self.__send_file(self.documents_url+self.images[selected-1])
        return 'Home'


def main():
    # Inicio de la conexión por Sockets
    menu = 'Home'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.connect((HOST, PORT))
        while True:
            if menu == 'Home':
                home = Home()
                menu = home.show_screen()
                commando = Comammad(sck, menu, HOST, PORT)
                commando.send_command()
            elif menu == 'Send':
                send = Send(sck, DOCUMENTS, 'hola')
                menu = send.send_file()
            elif menu == 'Download':
                download = Download(sck, DOCUMENTS)
                menu = download.download()
            elif menu == 'Close':
                print('Conexión cerrada')
                break


if __name__ == '__main__':
    main()
