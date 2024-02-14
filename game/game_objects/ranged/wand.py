from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from .ranged_weapon import RangedWeapon
from ..projectile import WandProjectile

if TYPE_CHECKING:
    from game.actors import Character


class Wand(RangedWeapon):
    projectile = WandProjectile
    unlock_score = 1300


def generate_wand(display: pygame.Surface, owner: Character):
    return Wand(image_path="resources/weapons/upg_wand.png",
               damage_points=100,
               hitbox_radius=180,
               display=display,
               owner=owner,
               fire_rate=15)