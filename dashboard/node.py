import pygame as pg


class Node:
    def __init__(self, node_handler: ..., position: tuple=(0, 0)):
        """
        Dashboard element for a context element (Agent, Task)
        """

        # Parent references
        self.node_handler = node_handler
        self.grid = node_handler.ui.grid
        self.preferences = self.node_handler.ui.preferences

        self.x, self.y = position
        self.width, self.height = 2, 2
        self.color = (100, 225, 125)

    def draw(self) -> None:
        """
        Draws the node to the grid surf
        """

        surf = self.grid.surf
        r = int((self.grid.scale / 20) + 1)
        pg.draw.rect(surf, self.preferences.secondary_color, self.grid.world_to_surf((self.x - self.width/2, self.y + self.height/2, self.width, self.height)), border_radius=r)
        pg.draw.rect(surf, self.preferences.tertiary_color, self.grid.world_to_surf((self.x - self.width/2, self.y + self.height/2, self.width, self.height)), r//2+1, border_radius=r)
        pg.draw.rect(surf, self.color, self.grid.world_to_surf((self.x - self.width/2, self.y + self.height/2, self.width, .25)), border_top_left_radius=r, border_top_right_radius=r)

    def collide(self, x, y) -> bool:
        return self.x - self.width/2 < x < self.x + self.width/2 and self.y - self.height/2 < y < self.y + self.height/2