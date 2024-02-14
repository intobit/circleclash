import pygame

from game.ui.weapon_image import Weapon_img
from game.game_objects.weapon import Weapon


class WeaponBar:
    """WeaponBar Class"""

    def __init__(self, display: pygame.Surface, weapons: list[Weapon]):
        """WeaponBar Class"""
        self.weapons = []
        self.display = display
        for weapon in weapons:
            self.weapons.append(Weapon_img(self.display, weapon))
        self.length = len(weapons) * 60
        self.cord = (display.get_width() // 2 - self.length // 2, display.get_height() - 90)
        self.font = pygame.font.SysFont('comicsansms', 12)

    def draw(self, score: int) -> None:
        """
        Draws the Weapons.
        :return:
        """
        overlay = pygame.Surface((self.length, 80))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120)

        self.display.blit(overlay, self.cord)
        for index, weapon in enumerate(self.weapons):
            weapon.update(score, (self.cord[0] + 20 + 60 * index, self.cord[1] + 10))

    def update(self, score: int) -> None:
        """
        Updates the map based on the Player.
        :return:
        """
        self.draw(score=score)

