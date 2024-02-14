from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from .ranged_weapon import RangedWeapon

if TYPE_CHECKING:
    from game.actors import Character


class Bow(RangedWeapon):
    unlock_score = 750
    pass


def generate_bow(display: pygame.Surface, owner: Character):
    return Bow(image_path="resources/weapons/upg_bow.png",
               damage_points=30,
               hitbox_radius=180,
               display=display,
               owner=owner,
               fire_rate=10)
