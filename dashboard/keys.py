import pygame as pg


class Keys:
    def __init__(self, ui):
        """
        Wrapperfor pygame keyboard input
        """
        
        self.ui = ui
        self.pressed  = pg.key.get_pressed()
        self.previous = self.pressed

    def update(self):
        """
        Updates the pressed key states
        """
        
        self.previous = self.pressed
        self.pressed = pg.key.get_pressed()

    def __getitem__(self, index: int) -> bool:
        return self.pressed[index]