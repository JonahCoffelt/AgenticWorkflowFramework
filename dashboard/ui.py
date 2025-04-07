import pygame as pg
from .preferences import Preferences
from .viewport import Viewport
from .grid import Grid
from .mouse import Mouse
from .keys import Keys
from .node_handler import NodeHandler


class UIHandler:
    preferences: Preferences
    """"""
    viewport: Viewport
    """"""
    def __init__(self, dashboard):
        """
        Handles all UI input and display for the dashboard
        """
        
        self.dashboard = dashboard
        self.win = dashboard.win

        # Handlers
        self.preferences  = Preferences()
        self.viewport     = Viewport(self, 0.05, .2, .15, .2)
        self.grid         = Grid(self)
        self.node_handler = NodeHandler(self)
        self.mouse        = Mouse(self)
        self.keys         = Keys(self)

    def draw(self):
        """
        Draw the dashboard UI to the screen
        """
        
        self.win.fill(self.preferences.primary_color)

        self.viewport.draw()

        self.grid.draw()
        self.node_handler.draw()
        self.grid.show()

    def update(self):
        """
        Update the UI and handle all inputs
        """
        
        # Get all inputs
        self.events = pg.event.get()
        self.mouse.update()
        self.keys.update()

        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.VIDEORESIZE:
                self.dashboard.win_size = (event.w, event.h)
                self.grid.set_surf()
            if event.type == pg.MOUSEWHEEL:
                self.mouse.scroll(event.y)

    def convert_rect(self, rect, padding=None):
        w, h = self.dashboard.win_size
        p = padding if padding != None else self.preferences.padding
        return (rect[0] * w + p, rect[1] * h + p, rect[2] * w - p * 2, rect[3] * h - p * 2)