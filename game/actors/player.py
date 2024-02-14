from math import pi, atan2

import pygame
from pygame.locals import *

from .character import Character, CharacterState
from game.game_objects import generate_prime_sword, generate_wooden_sword
from game.utilities.events import PLAYER_KILLED_EVENT
from game.game_objects.melee.axe import generate_double_edged_axe, generate_single_edged_axe
from game.game_objects.ranged.bow import generate_bow
from game.game_objects.ranged.wand import generate_wand


class Player(Character):
    """Player class

    This class represents the player. It inherits from Character and implements the necessary abstract methods.
    """
    initial_health = 1_000.0

    def __init__(self, *args, **kwargs):
        """
        Player class
        """
        super().__init__(*args, **kwargs)
        self.speed = 3
        # give the Player some initial weapons
        self.unlockable_weapons = []
        for weapon in [generate_wooden_sword(display=self.display, owner=self),
                       generate_prime_sword(display=self.display, owner=self),
                       generate_single_edged_axe(display=self.display, owner=self),
                       generate_double_edged_axe(display=self.display, owner=self),
                       generate_bow(display=self.display, owner=self),
                       generate_wand(display=self.display, owner=self)
                       ]:
            self.unlockable_weapons.append(weapon)
        self._check_new_weapon_unlock(0)
        self.draw()

    @Character.health.setter
    def health(self, value: float):
        """Changes the Player's health

        If the Player's state changes to KILLED, a PLAYER_KILLED_EVENT is fired to end the game (only on change so the
        event isn't triggered more than once).

        :param value: new health
        """
        value = max(0.0, value)
        new_state = self._get_future_state_from_health(value)
        if new_state == CharacterState.KILLED and self.state != new_state:
            pygame.event.post(pygame.event.Event(PLAYER_KILLED_EVENT))
        self.state = new_state
        self._health = value

    def _calculate_rotation(self) -> None:
        """Determines the Player's rotation from mouse position

        Calculates the Player's image/aiming rotation based on the mouse position on screen using atan2.
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        delta = mouse_pos - self.position
        rotation = (180 / pi) * -atan2(delta.y, delta.x)
        self.rotation = (0 - rotation) % 360

    def _check_new_weapon_unlock(self, score: int):
        for weapon in self.unlockable_weapons:
            if weapon.unlock_score <= score and weapon not in self.weapons.sprites():
                self.weapons.add(weapon)

    def reset(self):
        super().reset()
        self.weapons.empty()
        self._active_weapon_idx = 0

    def move(self) -> None:
        """Moves the player based on keyboard input

        Calculates a movement vector based on the user's input on the keyboard.
        """
        directions = self._get_movement_vector()
        self.position += directions * self.speed

    @staticmethod
    def _get_movement_vector() -> pygame.Vector2:
        """
        Derives a movement vector from the currently pressed keys

        Keyboard inputs are checked to create movement vector. This vector is normalized, so it can be multiplied with
        'speed' when moving the Player.

        :return: Vector2 representing the movement directions
        """
        keys = pygame.key.get_pressed()
        delta_x, delta_y = 0, 0
        if keys[K_LEFT] or keys[K_a]:
            delta_x -= 1
        if keys[K_UP] or keys[K_w]:
            delta_y -= 1
        if keys[K_RIGHT] or keys[K_d]:
            delta_x += 1
        if keys[K_DOWN] or keys[K_s]:
            delta_y += 1
        vector = pygame.Vector2(delta_x, delta_y)
        if not vector.x == 0 and vector.y == 0:
            return vector.normalize()
        return vector

    def update(self, score: int, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self._check_new_weapon_unlock(score)
