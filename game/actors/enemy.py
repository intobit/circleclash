from math import pi, atan2
from abc import ABC

import pygame
import random

from .character import Character, CharacterState
from .player import Player
from game.utilities.events import ENEMY_KILLED_EVENT, ENEMY_DESPAWN_EVENT
from ..utilities import GameState
from game.game_objects.ranged.bow import generate_bow, Bow


class Enemy(Character, ABC):
    def __init__(self, target: Player, points: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.points = points
        self.enemies = pygame.sprite.Group()
        self.draw()

    @Character.health.setter
    def health(self, value: float):
        value = max(0.0, value)
        new_state = self._get_future_state_from_health(value)
        if new_state == CharacterState.KILLED and self.state != new_state:
            kill_event = pygame.event.Event(ENEMY_KILLED_EVENT)  # create an ENEMY_KILLED_EVENT
            kill_event.killed = self  # attach the killed enemy (self) to the event
            pygame.event.post(kill_event)  # fire the event so the Player gets points based on the enemy
            despawn_event = pygame.event.Event(ENEMY_DESPAWN_EVENT)  # set a timer so the Enemy is despawned from the game
            despawn_event.killed = self
            pygame.time.set_timer(despawn_event, 2_000)
        self.state = new_state
        self._health = value

    @property
    def vector_to_target(self) -> pygame.Vector2:
        """Vector from Enemy to Player

        Calculates the vector from the Enemy to its target/the Player. The vector is normalized (so its length is 1)
        so it can be multiplied with the 'speed' attribute when the Enemy is moved.

        :return: Vector from Enemy to Player
        """
        return (self.target.position - self.position).normalize()

    def _calculate_rotation(self):
        """Determines the Enemy's rotation from the Player position

        Calculates the Enemy's image/aiming rotation based on the Player's and its own position. Atan2 is used to
        calculate the rotation from the vector_to_target property.
        """
        rotation = (180 / pi) * -atan2(self.vector_to_target.y, self.vector_to_target.x)
        self.rotation = (0 - rotation) % 360

    def move(self):
        """Moves the Enemy towards the Player, if the Player is alive"""
        if self.target.is_alive:
            delta = self.vector_to_target
            distance = (self.target.position - self.position).length()
            if self.active_weapon is not None and distance >= self.active_weapon.hitbox_radius:
                self.position += self.speed * delta
            if self.active_weapon and distance < self.active_weapon.hitbox_radius:
                self.attack()

    def _generate_unique_speed(self, min_speed, max_speed):
        """Creates for every enemy in a wave, a unique speed"""
        speeds = [enemy.speed for enemy in self.enemies.sprites()]
        while True:
            speed = random.uniform(min_speed, max_speed)
            if speed not in speeds:
                return speed


class Enemy1(Enemy):
    initial_health = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = 150
        self.initial_health = self.health
        self.speed = self._generate_unique_speed(1.8, 2.5)


class Enemy2(Enemy):
    initial_health = 80

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = 200
        self.initial_health = self.health
        self.speed = self._generate_unique_speed(1.5, 2)


class Enemy3(Enemy):
    initial_health = 120

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = 250
        self.initial_health = self.health
        self.speed = self._generate_unique_speed(1, 1.5)


class Enemy4(Enemy):
    initial_health = 1_000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = 300
        self.initial_health = self.health
        self.speed = self._generate_unique_speed(1.2, 1.2)

    def update(self, game_state: GameState, *args, **kwargs) -> None:
        super().update(game_state, *args, **kwargs)
        if self.health < self.initial_health / 2 and not isinstance(self.active_weapon, Bow):
            self.weapons.add(generate_bow(self.display, self))
            self.active_weapon_idx += 1
