import socket
from threading import Thread
from typing import Any


class Server:
    def __init__(self, host: str, port: int, listen_size=255) -> None:

        self.host = host
        self.port = port

        # Set up the server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to bind the server
        try:
            self.server.bind((host, port))
            self.server.listen(listen_size)
        # Server failed to bind
        except socket.error as e:
            print(f'Failed to start the server: {e}')
            return

        self.start()

    def start(self) -> None:
        """
        Starts the server loop
        """
        
        print('Server Started')
        self.running = True

        while self.running:
            self.update()

        self.server.close()

    def update(self) -> None:
        """
        Updates the server, checking for connections
        """

        try:
            client = self.server.accept()
            print(f'Connected to: {client[1]}')
        except KeyboardInterrupt:
            print("Server shutting down.")
            self.running = False
            return
        except Exception as e:
            print(f"Error during accept: {e}")
            return

        thread = Thread(target=self.client_thread, args=(client, ))
        thread.start()

    def client_thread(self, client: tuple[socket.socket, Any]) -> None:
        """
        Starts and maintains a connection with a client
        """

        connection, address = client

        # Send connection message
        connection.send(f'Connected with server at {self.host} : {self.port}'.encode('utf-8'))

        while True:
            try:
                data = connection.recv(2048).decode('utf-8')
                print(f'Recived {data} from {address}')
                connection.send(f'Recived: {data}'.encode('utf-8'))
            except:
                break

        print(f'Client at {address} disconnected')
        connection.close()

server = Server('10.246.122.144', 5050)