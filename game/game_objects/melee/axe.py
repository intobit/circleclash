from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from .melee_weapon import MeleeWeapon
from game.game_objects.projectile import AxeProjectile, DoubleAxeProjectile

if TYPE_CHECKING:
    from game.actors import Character


class Axe(MeleeWeapon):
    unlock_score = 200
    projectile = AxeProjectile

    def __init__(self, hitbox_angle: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hitbox_angle = hitbox_angle

    def attack(self, angle):
        num_projectiles = self.hitbox_angle // 60
        num_projectiles_per_side = (num_projectiles - 1) // 2
        shooting_angle = angle - num_projectiles_per_side * 60  # initial shooting angle
        start_position = pygame.Vector2(self.owner.actor.centerx, self.owner.actor.centery)
        for _ in range(num_projectiles):
            hitbox = self.projectile(start_pos=start_position, angle=shooting_angle, display=self.display)
            self.fired_projectiles.add(hitbox)
            shooting_angle += 60
        return hitbox


class DoubleAxe(Axe):
    unlock_score = 500
    projectile = AxeProjectile


def generate_single_edged_axe(display: pygame.Surface, owner: Character):
    return Axe(image_path="resources/weapons/axe2.png",
               damage_points=30,
               hitbox_angle=180,
               hitbox_radius=100,
               display=display,
               owner=owner,
               fire_rate=10)


def generate_double_edged_axe(display: pygame.Surface, owner: Character):
    return DoubleAxe(image_path="resources/weapons/axeDouble2.png",
                     damage_points=30,
                     hitbox_angle=360,
                     hitbox_radius=100,
                     display=display,
                     owner=owner,
                     fire_rate=10)


