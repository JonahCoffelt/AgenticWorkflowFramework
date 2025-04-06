import pygame as pg


class Node:
    def __init__(self, node_handler: ...):
        """
        Dashboard element for a context element (Agent, Task)
        """
        self.node_handler = node_handler

    def draw(self) -> None:
        ...