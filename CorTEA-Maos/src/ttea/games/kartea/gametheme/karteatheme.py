import pygame

from ttea.games.gametheme.basetheme import BaseTheme


class KarTEATheme(BaseTheme):
    """Encapsula o esquema de cores da pista."""

    def __init__(self):
        self.finish = {
            "dark": pygame.Color(0, 0, 0),
            "light": pygame.Color(255, 255, 255),
        }
        self.grass = {
            "dark": pygame.Color(0, 154, 0),
            "light": pygame.Color(16, 200, 16),
        }
        self.rumble = {
            "dark": pygame.Color(255, 0, 0),
            "light": pygame.Color(255, 255, 255),
        }
        self.road = {
            "dark": pygame.Color(75, 75, 75),
            "light": pygame.Color(107, 107, 107),
        }
