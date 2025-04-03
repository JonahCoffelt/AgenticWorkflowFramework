from .networker import Networker


class Client(Networker):
    def __init__(self, callback=None):
        super().__init__(callback)
