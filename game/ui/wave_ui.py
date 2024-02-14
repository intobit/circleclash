import pygame
from game.utilities.gamestate import GameState


class Wave_ui:
    """Wave Class"""

    def __init__(self, display: pygame.Surface):
        """Wave Class"""
        self.display = display
        self.font = pygame.font.SysFont('comicsansms', 20)

        self.wave_cor = (self.display.get_width() // 2 - 40, 2)

    def draw(self, wave: int) -> None:
        """
        Draws the Wave.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        life_text = self.font.render(f'WAVE {wave}', True, (255, 255, 255))
        self.display.blit(life_text, self.wave_cor)


    def update(self, wave: int, state: GameState) -> None:
        """
        Updates the Wave based on the Player.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        if state is not GameState.READY:
            self.draw(wave=wave)

