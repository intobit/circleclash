import pygame
from game.utilities import GameState

class UpperBar:
    """UpperBar Class"""

    def __init__(self, display: pygame.Surface, height: int):
        """UpperBar Class"""
        self.display = display
        self.height = height


    def draw(self) -> None:
        """
        Draws the UpperBar.
        :return:
        """
        overlay = pygame.Surface((self.display.get_width(), self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(220)

        self.display.blit(overlay, (0, 0))

    def update(self, state: GameState) -> None:
        """
        Updates the UpperBar based on the .
        :return:
        """
        if state is GameState.RUNNING:
            self.draw()

