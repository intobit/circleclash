from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
import math

import pygame

from game.utilities import read_image, GameState, rotate_image
from game.game_objects.projectile import Projectile

if TYPE_CHECKING:
    from game.actors import Character


class Weapon(pygame.sprite.Sprite, ABC):
    projectile = Projectile
    unlock_score = 0

    def __init__(self, image_path, damage_points, hitbox_radius, display, owner: Character, fire_rate: int):
        super().__init__()
        self.image = read_image(image_path)
        self.damage_points = damage_points
        self.display = display
        self.owner = owner
        self.rect = None
        self.hitbox_radius = hitbox_radius
        self.fired_projectiles = pygame.sprite.Group()
        self.fire_rate = fire_rate

    def draw(self, angle: int):
        # TODO: rotate weapon based on owner's rotation
        angle = (360 - angle) % 360 - 135
        img = rotate_image(self.image.copy(), angle)
        x = math.cos(angle)
        y = math.sin(angle)
        draw_pos = (self.owner.actor.x + x, self.owner.actor.y)
        self.rect = self.display.blit(img, draw_pos)

    def update(self, game_state: GameState, angle: int):
        self.fired_projectiles.update(game_state)
        self.draw(angle=angle)

    def attack(self, angle):
        # Fire a new projectile
        start_position = pygame.Vector2(self.rect.centerx, self.rect.centery)
        projectile = self.projectile(start_pos=start_position, angle=angle, display=self.display)
        self.fired_projectiles.add(projectile)
        return projectile
