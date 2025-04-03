import socket

IP = '127.0.0.1'
PORT = 5050


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str) -> str:
        self.socket.sendto(message.encode('utf-8'), (IP, PORT))

        # return self.listen()

    def listen(self) -> str:
        data, address = self.socket.recvfrom(1024)

        print('got: ' + data.decode('utf-8'))

        return data.decode('utf-8')

    def __del__(self) -> None:
        self.socket.close()