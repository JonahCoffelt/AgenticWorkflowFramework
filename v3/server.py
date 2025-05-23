from .networker import Networker, IP, PORT


class Server(Networker):
    def __init__(self, callback=None):
        super().__init__(callback)
        self.socket.bind((IP, PORT))