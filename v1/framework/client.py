import socket
import time

class Client:
    def __init__(self, host: str, port: int):

        # Set up the server socket        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to connect
        try:
            self.server.connect((host, port))
        # Failed to connect to the server
        except:
            print(f'Client failed to connect to the server at: {host, port}')

        # Get the connection message
        self.server.recv(2048).decode('utf-8')

    def send(self, data: str) -> str:
        try:
            self.server.send(data.encode('utf-8'))
        except socket.error as e:
            print(f"Client send error: {e}")

        return self.server.recv(2048).decode('utf-8')    

client = Client('10.246.122.144', 5050)

client.send('hi')
client.send('there')

time.sleep(2)