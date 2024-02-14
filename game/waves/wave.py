import pygame
import random

from game.actors import Player
from game.utilities import GameState
from game.game_objects.projectile import Projectile


class Wave:
    def __init__(self, display: pygame.Surface, target: Player, enemies_to_spawn: dict):
        self.display = display
        self.target = target
        self.spawned_enemies = pygame.sprite.Group()
        self.enemies_to_spawn = enemies_to_spawn
        self.spawned = False

    @property
    def is_complete(self) -> bool:
        if not self.spawned:
            return False
        for enemy in self.spawned_enemies.sprites():
            if enemy.is_alive:
                return False
        return True

    def spawn_enemies(self) -> None:
        if self.spawned:
            return

        # dictionary: key = Enemy class, value = tupel (num_enemies, Weapon)
        for enemy_cls, enemy_vals in self.enemies_to_spawn.items():
            for i in range(enemy_vals[0]):
                enemy = enemy_cls(position=(random.randint(0, 1200), random.randint(0, 1200)),
                                  target=self.target, display=self.display)
                weapon_fun = enemy_vals[1]
                weapon = weapon_fun(display=self.display, owner=enemy)
                enemy.weapons.add(weapon)
                self.spawned_enemies.add(enemy)
        self.spawned = True

    def update(self, game_state: GameState, projectiles: [Projectile]) -> None:
        self.spawned_enemies.update(game_state)
        for enemy in self.spawned_enemies:
            enemy.calc_new_health(projectiles)
