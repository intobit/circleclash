from game.game_objects.weapon import Weapon
from game.game_objects.projectile import MeleeProjectile


class MeleeWeapon(Weapon):
    projectile = MeleeProjectile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
