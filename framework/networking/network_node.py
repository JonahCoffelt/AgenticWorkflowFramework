import socket
from threading import Thread

IP = '127.0.0.1'
PORT = 5051


class NetworkNode:
    def __init__(self, ip: str=IP, port: int=PORT) -> None:
        """
        General class for implementing agents or things that can interact with the network.
        """

        # Start the server
        self.socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind
        self.socket.bind((ip, port))
        # Get address for reference
        self.address = self.socket.getsockname()

        # Start a thread
        self.start()

    def start(self) -> None:
        """
        Starts a listen loop thread
        """

        thread = Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self) -> None:
        """
        Simple listen loop
        """
        
        self.running = True
        while self.running:
            try:
                self.listen()
            except OSError:
                self.running = False

    def send(self, data: bytes | bytearray | str, address: tuple[str, int]=(IP, PORT)) -> None:
        """
        Sends a message to the given address (ip, port).
        Defaults to the sever.
        """

        if isinstance(address, NetworkNode): address = address.address

        # Encode content if needed
        if isinstance(data, str): data = data.encode('utf-8')

        # Send out
        self.socket.sendto(data, address)

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """
        Processes a recived message. 
        This method should most likely be overridden. 
        """

        print(f'Recived "{data.decode('utf-8')}" from {address}')

    def listen(self) -> None:
        """
        Listens for incoming messages
        """

        data, address = self.socket.recvfrom(10_000)
        self.receive(data, address)

    def close(self) -> None:
        """
        closes the server socket
        """
        
        print("\nServer shutting down")
        self.running = False
        self.socket.close()

    def __del__(self) -> None:
        self.close()