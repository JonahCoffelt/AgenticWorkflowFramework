class Preferences:
    def __init__(self, 
                 primary_color:    tuple=(25, 25, 25), 
                 secondary_color:  tuple=(35, 35, 35), 
                 tertiary_color:   tuple=(45, 45, 45), 
                 background_color: tuple=(75, 75, 75), 
                 font_color:       tuple=(225, 225, 225), 
                 font_size:        int=16,
                 radius:           int=10,
                 padding:          int=6):
        """
        Container for all the dashboard preferences
        """
        self.primary_color:    tuple = primary_color
        self.secondary_color:  tuple = secondary_color
        self.tertiary_color:   tuple = tertiary_color
        self.background_color: tuple = background_color
        self.font_color:       tuple = font_color
        self.font_size:        int   = font_size
        self.radius:           int   = radius
        self.padding:          int   = padding