import pygame as pg
from pygame import freetype

class FontRenderer():
    font: freetype.Font
    def __init__(self):
        freetype.init()
        self.font = freetype.Font('dashboard/assets/Roboto-Regular.ttf', 72)
        self.font.antialiased = True

    def render(self, text, color=(255, 255, 255), bold=False, underline=False, italic=False):
        """
        Renders any font which has been loaded to the class instance.
        Args:
            text:str
                Text to be rendered
            color:(int, int, int) =(255, 255, 255)
                The RGB value of the text
            bold:bool (=False)
                Specifies if the text should be rendered in bolded font
            underline:bool (=False)
                Specifies if the text should be underlined in bolded font
            italic:bool (=False)
                Specifies if the text should be rendered in italicized font
        """

        self.font.strong    = bold
        self.font.underline = underline
        self.font.oblique   = italic

        return self.font.render(text, color, (0, 0, 0, 0))[0]