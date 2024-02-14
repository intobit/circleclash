from os import path

import pygame

from game.game_objects.weapon import Weapon
from game.utilities.helper_functions import read_image


class Weapon_img:
    """Weapon_img Class"""

    def __init__(self, display: pygame.Surface, weapon: Weapon):
        """Weapon_img Class"""
        self.weapon = weapon
        self.img_question_mark = read_image(path.join("resources", "icons", "question_mark.png"))
        self.img_question_mark = pygame.transform.scale(self.img_question_mark, (30, 30))
        self.img = pygame.transform.scale(weapon.image, (30, 30))
        self.display = display
        self.font = pygame.font.SysFont('comicsansms', 8)

    def draw(self, img, radius, damage , cord: (int, int)) -> None:
        """
        Draws the Weapon_img.
        :return:
        """
        self.display.blit(img, cord)

        damage_text = self.font.render('Damage', True, (255, 255, 255))
        self.display.blit(damage_text, (cord[0] - 10, cord[1] + 10))
        damage_value = self.font.render(f'{damage}', True, (255, 255, 255))
        self.display.blit(damage_value, (cord[0] - 10, cord[1] + 20))

        radius_text = self.font.render('Radius', True, (255, 255, 255))
        self.display.blit(radius_text, (cord[0] - 10, cord[1] + 30))
        radius_value = self.font.render(f'{radius}', True, (255, 255, 255))
        self.display.blit(radius_value, (cord[0] - 10, cord[1] + 40))

    def update(self, score: int, cord: (int, int)) -> None:
        """
        Updates the map based on the Player.
        :return:
        """
        if self.weapon.unlock_score <= score:
            self.draw(self.img, self.weapon.hitbox_radius, self.weapon.damage_points, cord)
        else:
            self.draw(self.img_question_mark, "??", "??", cord)

