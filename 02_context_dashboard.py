import framework as fmk
import pygame as pg
from dashboard.ui import UIHandler


class Dashboard:
    def __init__(self):
        """
        UI wrapper for the context
        """
        
        self.win_size = (800, 800)
        self.win = pg.display.set_mode(self.win_size, flags=pg.RESIZABLE)
        self.clock = pg.Clock()

    def draw(self):
        """
        Draws all the elements of the dashboard
        """
        
        self.ui.draw()
        pg.display.flip()

    def update(self):
        """
        Updates the dashboard and handels
        """
        
        self.ui.update()
        self.dt = self.clock.tick(60) / 1000

    def start(self):
        """
        Start the dashbaord app. 
        Starts the context server.
        """

        # Create a context
        self.ctx = fmk.Context()
        self.ctx.add_task((None, None), "Test Task", [])

        # Create a UI handler
        self.ui = UIHandler(self)

        # Start update loop for dashboard
        self.running = True
        while self.running:
            self.update()
            self.draw()

        self.ctx.running = False


dashboard = Dashboard()
dashboard.start()