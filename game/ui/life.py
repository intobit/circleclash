from os import path

import pygame

from game.actors import Player
from game.utilities.helper_functions import read_image
from game.utilities.gamestate import GameState


class Life:
    """Life Class"""

    def __init__(self, display: pygame.Surface):
        """Life Class"""
        self.img = read_image(path.join("resources", "icons", "heart.png"))
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.display = display
        self.font = pygame.font.SysFont('comicsansms', 20)

    def draw(self, player: Player) -> None:
        """
        Draws the life.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        self.display.blit(self.img, (0, 1))
        life_text = self.font.render(f'{int(player.health)}', True, (255, 0, 0))
        self.display.blit(life_text, (40, 1))


    def update(self, player: Player, state: GameState) -> None:
        """
        Updates the map based on the Player.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        if state is not GameState.READY:
            self.draw(player=player)

