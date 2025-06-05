import socket
from socket import socket as SocketType  # for type hinting
from threading import Thread

IP = '127.0.0.1'
PORT = 5051


class NetworkNode:
    """
    A base class for network nodes that can send and receive UDP messages.
    Provides basic socket handling, binding, and a background listening thread.
    """

    socket: SocketType
    address: tuple[str, int]
    running: bool

    def __init__(self, ip: str=IP, port: int=PORT) -> None:
        """
        Initializes the network node, binds the socket, and starts a listen thread.

        Args:
            ip (str): The IP address to host the socket on. Defaults to '127.0.0.1'.
            port (int): The port number to host the socket on. Defaults to 5051.
        """

        # Initalize running state
        self.running = False

        # Start the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind
        self.socket.bind((ip, port))
        # Get address for reference
        self.address = self.socket.getsockname()

        # Start a thread
        self.start()

    def start(self) -> None:
        """Creates and starts a listen loop thread"""

        thread = Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self) -> None:
        """Infinte listen loop used for thread creation"""
        
        self.running = True
        while self.running:
            try:
                self.listen()
            except OSError:
                self.running = False

    def send(self, data: bytes | bytearray | str, address: tuple[str, int]=(IP, PORT)) -> None:
        """
        Sends a message to the given address (ip, port). Defaults to the sever.
        Args:
            data (bytes | bytearray | str): The information to be sent
            address: (tuple[str, int]): The address of the node to recive the information
                                        Can also be a NetworkNode instance.
        """

        # Accept a NetworkNode as address, just extract the address
        if isinstance(address, NetworkNode): 
            address = address.address

        # Encode content if needed
        if isinstance(data, str): 
            data = data.encode('utf-8')

        # Send out
        self.socket.sendto(data, address)

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """
        Processes a recived message. 
        
        This method should most likely be overridden. 
        """

        print(f'Recived "{data.decode('utf-8')}" from {address}')

    def listen(self) -> None:
        """Listens for incoming messages"""

        data, address = self.socket.recvfrom(10_000)
        self.receive(data, address)

    def close(self) -> None:
        """Closes the server socket and stops the listening thread."""
        
        print("\nServer shutting down")
        self.running = False
        self.socket.close()