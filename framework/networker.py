import socket


IP = '127.0.0.1'
PORT = 5051


class Networker:
    def __init__(self, callback=None):
        """
        Abstract class for implementing agents or things that can interact with the network.
        Used to implement server and client.
        """

        # Start the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Used to callback when messages are recived
        self.callback = callback

    def send(self, data: bytes | bytearray | str, ip: str=None, port: int=None) -> str:
        """
        Sends a message to the given IP and port.
        Defaults to the sever.
        """
        
        ip = ip if ip else IP
        port = port if port else PORT

        if isinstance(data, str): data = data.encode('utf-8')

        self.socket.sendto(data, (ip, port))

    def listen(self):
        """
        Listens for incoming messages
        """

        data, address = self.socket.recvfrom(1024)
        self.callback(data, address)

    def close(self):
        """
        closes the server socket
        """
        
        print("\nServer shutting down")
        self.socket.close()

    def __del__(self):
        self.close()