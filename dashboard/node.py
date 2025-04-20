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

        if not self.in_view(): return

        surf = self.grid.surf
        font = self.node_handler.ui.font
        r = int((self.grid.scale / 20) + 1)
        h = self.grid.scale * .5
        p = r//2+1
        th = h - p * 2

        # Render the box and outline
        rect = self.grid.world_to_surf((self.x - self.width/2, self.y + self.height/2, self.width, self.height))
        pg.draw.rect(surf, self.preferences.secondary_color, rect, border_radius=r)
        pg.draw.rect(surf, self.preferences.tertiary_color, rect, r//2+1, border_radius=r)
        
        # Draw top bar
        pg.draw.rect(surf, self.color, (*rect[:3], h), border_top_left_radius=r, border_top_right_radius=r)

        # Draw title
        title_surf = font.render("Task")
        title_rect = title_surf.get_rect()
        title_surf = pg.transform.scale(title_surf, (title_rect[2] / title_rect[3] * th, th))
        surf.blit(title_surf, (rect[0] + p * 2, rect[1] + p))

        # Draw Connector Ports
        pg.draw.circle(surf, self.color, (rect[0]          , rect[1] + rect[3] // 2), h // 5)
        pg.draw.circle(surf, self.color, (rect[0] + rect[2], rect[1] + rect[3] // 2), h // 5)


    def in_view(self) -> bool:
        """
        Checks if the node is in view
        """
        
        rect = self.grid.world_to_surf((self.x - self.width/2, self.y + self.height/2, self.width, self.height))
        w, h = self.grid.width, self.grid.height

        return rect[0] + rect[2] > 0 and rect[0] < w and rect[1] + rect[3] > 0 and rect[1] < h

    def collide(self, x, y) -> bool:
        return self.x - self.width/2 < x < self.x + self.width/2 and self.y - self.height/2 < y < self.y + self.height/2