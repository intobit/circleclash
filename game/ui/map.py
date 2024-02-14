from os import path

import pygame

from game.actors import Player
from game.utilities.helper_functions import read_image


class Map:
    """Map Class

    Stores a map background as a surface that is read from the 'resources' folder.
    """

    def __init__(self, display: pygame.Surface):
        """Map Class"""
        self.img = read_image(path.join("resources", "maps", "new_map.jpg"))
        self.display = display

    def draw(self, player: Player) -> None:
        """
        Draws the background.

        The maps position is determined based on the Player's position. As the Player's position in the game windows
        is fixed, the map has to move behind it.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        win_size = self.display.get_size()
        map_size = self.img.get_size()
        x = -max(0, min(map_size[0] - win_size[0], player.actor.x))
        y = -max(0, min(map_size[1] - win_size[1], player.actor.y))
        self.display.blit(self.img, (x, y))

    def update(self, player: Player) -> None:
        """
        Updates the map based on the Player.

        :param player: Player instance used for placing the background correctly
        :return:
        """
        self.draw(player=player)
