import pygame as pg
import math


class Mouse:
    def __init__(self, ui):
        """
        Wrapper for pygame mouse inputs
        """
        self.ui = ui

        self.grab = False
        self.grab_position = (0, 0)
        self.buttons  = pg.mouse.get_pressed()
        self.previous_buttons = self.buttons

    def update(self):
        """
        Update the mouse state
        """
        
        # Update the mouse position
        self.position = pg.mouse.get_pos()
        self.previous_buttons = self.buttons
        self.buttons  = pg.mouse.get_pressed()

        self.set_viewport()

        if self.clicked:
            self.grab_position = self.position
            self.item = self.collide()
        elif self.held:
            self.hold()
            self.grab = True
        else:
            self.grab = False

    def scroll(self, y):
        """
        Scrolls the mouse
        """
        
        match self.viewport:
            case 'center':
                if y > 0:
                    self.ui.grid.scale = max(self.ui.grid.scale * 1 * 1.1, 10.0)
                else:
                    self.ui.grid.scale = max(self.ui.grid.scale * 1 / 1.1, 10.0)
                # print(self.ui.grid.scale)
            case 'top':
                ...
            case 'bottom':
                ...
            case 'left':
                ...
            case 'right':
                ...

    def collide(self):
        """
        Collides the mouse with the deshboard elements 
        """

        match self.viewport:
            case 'left edge':
                return 'left edge'
            case 'right edge':
                return 'right edge'
            case 'bottom edge':
                return 'bottom edge'
            case 'center':
                self.grid_start = self.ui.grid.position[:]
                self.mouse_start = self.position
                return 'grid'
            case 'top':
                ...
            case 'bottom':
                ...
            case 'left':
                ...
            case 'right':
                ...

    def hold(self):
        """
        
        """
        
        if isinstance(self.item, str):
            self.hold_string() 

    def hold_string(self):
        """
        
        """

        viewport = self.ui.viewport
        win_size = self.ui.dashboard.win_size

        match self.item:
            case 'left edge':
                viewport.left = min(self.x / win_size[0], 1 - viewport.right -.05)
                self.ui.grid.set_surf()
            case 'right edge':
                viewport.right = min(1 - self.x / win_size[0], 1 - viewport.left -.05)
                self.ui.grid.set_surf()
            case 'bottom edge':
                viewport.bottom = min(1 - self.y / win_size[1], 1 - viewport.top -.05)
                self.ui.grid.set_surf()
            case 'grid':
                x = self.grid_start[0] + (self.mouse_start[0] - self.position[0])
                y = self.grid_start[1] - (self.mouse_start[1] - self.position[1])

                self.ui.grid.x = x
                self.ui.grid.y = y

    def set_viewport(self):
        """
        Sets the viewport the mouse is in
        """

        viewport = self.ui.viewport
        w, h = self.ui.dashboard.win_size
        t = 10
        p = self.ui.preferences.padding

        if (1 - viewport.bottom) * h - t < self.y < (1 - viewport.bottom) * h + t:
            self.viewport = 'bottom edge'
        elif viewport.left * w - t < self.x + p < viewport.left * w + t:
            self.viewport = 'left edge'
        elif (1 - viewport.right) * w - t < self.x - p < (1 - viewport.right) * w + t:
            self.viewport = 'right edge'
        elif self.y < viewport.top * h:
            self.viewport = 'top'
        elif self.y > (1 - viewport.bottom) * h:
            self.viewport = 'bottom'
        elif self.x < viewport.left * w:
            self.viewport = 'left'
        elif self.x > (1 - viewport.right) * w:
            self.viewport = 'right'
        else:
            self.viewport = 'center'

    @property
    def clicked(self) -> bool:
        return self.buttons[0] and not self.previous_buttons[0]
    
    @property
    def held(self) -> bool:
        return self.buttons[0] and self.previous_buttons[0]

    @property
    def x(self) -> int:
        return self.position[0]
    
    @property
    def y(self) -> int:
        return self.position[1]