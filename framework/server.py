import socket
import sys

IP = '127.0.0.1'
PORT = 5050


class Server:
    def __init__(self, callback=None):
        """
        Encapsulates the server for an agent context.
        """

        # Start the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((IP, PORT))

        # Used to callback when messages are recived
        self.callback = callback

    def update(self):
        """
        Listens for incoming messages
        """

        data, address = self.socket.recvfrom(1024)
        ret = self.callback(data, address)

        print(f'sending back : {ret} to : {address}')
        self.socket.sendto(ret.encode('utf-8'), address)


    def close(self):
        """
        closes the server socket
        """
        
        print("\nServer shutting down")
        self.socket.close()

    def __del__(self):
        self.close()