from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from .melee_weapon import MeleeWeapon
from ..projectile import WoodenSwordProjectile, PrimeSwordProjectile

if TYPE_CHECKING:
    from game.actors import Character


class WoodenSword(MeleeWeapon):
    projectile = WoodenSwordProjectile


class PrimeSword(MeleeWeapon):
    projectile = PrimeSwordProjectile
    unlock_score = 100


def generate_wooden_sword(display: pygame.Surface, owner: Character):
    return WoodenSword(image_path="resources/weapons/swordWood.png",
                       damage_points=20,
                       hitbox_radius=35,
                       display=display,
                       owner=owner,
                       fire_rate=10)


def generate_prime_sword(display: pygame.Surface, owner: Character):
    return PrimeSword(image_path="resources/weapons/sword.png",
                      damage_points=50,
                      hitbox_radius=70,
                      display=display,
                      owner=owner,
                      fire_rate=10)

