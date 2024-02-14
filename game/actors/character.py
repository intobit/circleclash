from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
from os import path

import pygame

from game.utilities import GameState, read_image, rotate_image
from game.game_objects.weapon import Weapon
from game.game_objects.projectile import Projectile


class CharacterState(Enum):
    """Possible states of Character objects"""

    IMMOVABLE = 0
    """State when the game is paused or the game has ended."""

    DEFAULT = 1
    """Default CharacterState"""

    HIT = 2
    """State when the Character has been hit."""

    CRITICAL = 3
    """State when the Character's health is critical."""

    KILLED = 4
    """State when the Character has been killed."""


class Character(pygame.sprite.Sprite, ABC):
    """Abstract base class for Player and Enemy classes

    This is the base class for both Player and Enemy classes. A Character can move across the map, carry weapons and
    take damage (and die). Characters have a state (e.g., IMMOVABLE or DEFAULT) that determines what a Character can do.
    A IMMOVABLE Character e.g. cannot move anymore (when the game is paused). The image that is used for displaying the
    Character also depends on the Character's state (a CRITICAL Characters is surrounded by a red ring, while a killed
    one has a grey overlay).

    A Character's position is stored in the 'position' attribute. Characters move across the map with a certain speed
    ('speed' attribute). A start position can be passed when initializing an object. Since Character's can rotate, its
    current rotation is stored in the 'rotation' attribute. Two methods ('move' and '_calculate_rotation') have to be
    implemented in derived classes.

    All weapons a Character carries, are contained in the 'weapons' sprite group. The currently selected weapon is
    controlled via the 'active_weapon_index' attribute.
    """
    size = (64, 64)
    initial_health = 100.0

    def __init__(self, display: pygame.Surface, images: Optional[dict] = None, position: Optional[pygame.Vector2] = None, *args):
        """Abstract base class for Player and Enemy classes

        :param display: pygame.display used for rendering
        :param images: optional dictionary for passing custom images for different CharacterStates
        :param position: Character spawn location
        """
        super().__init__(*args)
        self.display = display
        self.position = position or pygame.Vector2(200, 200)
        self.speed = 5
        self.critical_health_limit = 0.2 * self.initial_health
        self.state = CharacterState.DEFAULT
        self._health = self.initial_health
        self.actor = None
        self.weapons = pygame.sprite.Group()
        self._active_weapon_idx = 0
        self.rotation = 0
        self.images = images or self._read_images()
        self.frames_since_last_attack = 0
        self.rect = self.images[CharacterState.DEFAULT].get_rect()

    @classmethod
    def _read_images(cls) -> dict[CharacterState, pygame.Surface]:
        """Reads the different images for the CharacterStates.

        Reads the images for the different CharacterStates from the 'resources' directory. There can be one png per
        CharacterState. Only the DEFAULT png has to be available. This image will be used for all states, where no
        image is available.

        :return: dictionary with CharacterStates as keys and pygame Surfaces as Values
        """
        base_directory = path.join("resources", "actors", cls.__name__)
        state_images = {}
        default = read_image(path.join(base_directory, "default.png"))
        state_images[CharacterState.DEFAULT] = default
        for state in CharacterState:
            filename = path.join(base_directory, f"{str(state.name).lower()}.png")
            if path.exists(filename):
                state_images[state] = read_image(filename)
            else:
                state_images[state] = default
        return state_images

    @property
    def active_weapon_idx(self) -> int:
        """Index of the currently selected weapon"""
        return self._active_weapon_idx

    @active_weapon_idx.setter
    def active_weapon_idx(self, value: int) -> None:
        """Changes the active_weapon_idx attribute

        :param value: new index
        """
        # only change weapon if Character is alive and movable and if there are weapons
        if self.weapons.sprites() and self.state not in [CharacterState.KILLED, CharacterState.IMMOVABLE]:
            # limit _active_weapon_idx (0 to self.weapons length -1) or set to -1 if no Weapon is equipped
            self._active_weapon_idx = int(value) % len(self.weapons.sprites()) if self.weapons.sprites() else -1

    @property
    def active_weapon(self) -> Optional[Weapon]:
        """Returns the currently selected weapon using active_weapon_idx"""
        if not self.weapons:
            return None
        weapon = self.weapons.sprites()[self.active_weapon_idx]
        return weapon

    @property
    def health(self) -> float:
        """Character health"""
        return self._health

    def calc_new_health(self, projectiles: [Projectile]):
        projectiles_hit = pygame.sprite.spritecollide(self, projectiles, True)
        for projectile in projectiles_hit:
            self.health -= projectile.damage_points

    @health.setter
    @abstractmethod
    def health(self, value: float) -> None:
        """Changes a Character's health

        Limits health values to values >= 0 and updates the Character's state based on its health.

        :param value: new health value
        """

    def _get_future_state_from_health(self, future_health: float) -> CharacterState:
        """
        Determines the future CharacterState based on the new health value.

        :param future_health: future health value
        """
        if 0 < future_health <= self.critical_health_limit:
            return CharacterState.CRITICAL
        elif future_health == 0.0:
            return CharacterState.KILLED
        elif future_health < self.health:
            return CharacterState.HIT
        return CharacterState.DEFAULT

    @property
    def is_critical(self) -> bool:
        """Returns True if the Character's health is below its critical health limit, False otherwise."""
        if 0 < self.health <= self.critical_health_limit:
            return True
        return False

    @property
    def is_alive(self) -> bool:
        """Returns True if the Character's health is above 0, False otherwise."""
        if 0 < self.health:
            return True
        return False

    def reset(self) -> None:
        """Resets the Character"""
        self.position = pygame.Vector2(200, 200)
        self.health = self.initial_health
        self.draw()

    @abstractmethod
    def _calculate_rotation(self) -> None:
        """Determines the rotation of the Character

        This method must set the Character's 'rotation' attribute that is used for rotating the Character's image and
        aiming.
        """

    def draw(self) -> None:
        """Renders the Player

        Chooses the correct image depending on the Character's state, rotates it based on the 'rotation' attribute and
        displays it. This method is called every tick.
        """
        img = self.images[self.state].copy()
        rot_img = rotate_image(img=img, angle=self.rotation)
        self.actor = self.display.blit(rot_img, self.position)
        self.rect = self.actor

    def attack(self) -> None:
        """Attacks with the Character's Weapon"""
        if self.state not in [CharacterState.KILLED, CharacterState.IMMOVABLE] and \
                self.frames_since_last_attack >= self.active_weapon.fire_rate:
            self.active_weapon.attack(angle=self.rotation)
            self.frames_since_last_attack = 0

    @abstractmethod
    def move(self) -> None:
        """Moves the Character

        This method must move the Character across the map either depending on user input or on the player's location.
        This method is called every tick.
        """

    def update(self, game_state: GameState, *args, **kwargs) -> None:
        """Method to run on tick

        This method changes a Character's state based on the game's current state (e.g., PAUSED or WIN). If the
        Character is able to move, '_calculate_rotation()' and 'move' are called.

        :param game_state: current GameState
        """
        if game_state in [GameState.READY, GameState.PAUSED, GameState.WIN]:
            self.state = CharacterState.IMMOVABLE
        elif game_state == GameState.RUNNING and self.state == CharacterState.IMMOVABLE:
            # if the game was paused, reset the Character's state to the correct state
            if self.is_critical:
                self.state = CharacterState.CRITICAL
            else:
                self.state = CharacterState.DEFAULT
        if self.state not in [CharacterState.KILLED, CharacterState.IMMOVABLE]:
            self._calculate_rotation()
            self.move()
        self.draw()
        if self.active_weapon:
            self.active_weapon.update(game_state, self.rotation)
        self.frames_since_last_attack += 1
