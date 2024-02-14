from game.game_objects.weapon import Weapon
from game.game_objects.projectile import RangedProjectile


class RangedWeapon(Weapon):
    projectile = RangedProjectile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 10
