from typing import Optional, List

import pygame

from game.utilities.events import WIN_EVENT, SPAWN_WAVE_EVENT
from game.actors.player import Player
from game.utilities.gamestate import GameState
from game.waves.wave import Wave
from game.game_objects.projectile import Projectile


class WaveManager:
    """Class for managing the individual waves

    This class contains and manages the different waves of enemies. The individual Wave objects are stored in a list.
    The currently active wave is determined using the '_active_wave_idx' attribute. When a wave is completed, the next
    one is spawned.
    """

    def __init__(
        self, display: pygame.Surface, target: Player, waves: Optional[List[Wave]] = None
    ):
        """Class for managing the individual waves

        :param waves: list of Wave objects to sequentially run through
        """
        self.target = target
        self.display = display
        self.waves = waves or []
        self._active_wave_idx = -1
        self.spawn_next_wave()

    @property
    def active_wave(self) -> Wave:
        """
        Returns the active Wave or None if no wave is currently active

        :return: currently active Wave or None
        """
        if self.waves and self._active_wave_idx is not None:
            return self.waves[self._active_wave_idx]

    def clear_current_wave(self) -> None:
        """Removes all enemies in the current wave"""
        for enemy in self.active_wave.spawned_enemies:
            enemy.kill()
    
    @property        
    def active_wave_index(self) -> int or None:
        """
        Returns the active Wave or None if no wave is currently active

        :return: currently active Wave Index or None
        """
        if self._active_wave_idx is not None:
            return self._active_wave_idx
        return None

    def clear_current_wave(self) -> None:
        """Removes all enemies in the current wave"""
        for enemy in self.active_wave.spawned_enemies:
            enemy.kill()

    def spawn_next_wave(self) -> None:
        """Spawns the next wave or ends the game

        Spawns a new wave if the '_active_wave_idx' counter is still in the range of the list of waves and the current
        wave is completed, or if the first wave hasn't been spawned yet (= on game start). If the current wave was the
        last wave, a WIN_EVENT is fired.
        """
        if (self._active_wave_idx < len(self.waves) - 1 and self.active_wave.is_complete) or \
                (self._active_wave_idx == -1 and self.active_wave.spawned is False):
            self._active_wave_idx += 1
            self.active_wave.spawn_enemies()
            pygame.event.post(pygame.event.Event(SPAWN_WAVE_EVENT))
        elif self.active_wave and self.active_wave.is_complete:
            pygame.event.post(pygame.event.Event(WIN_EVENT))

    def reset(self) -> None:
        """Resets the WaveManager to the first wave"""
        self.clear_current_wave()
        self._active_wave_idx = 0
        for wave in self.waves:
            wave.spawned = False
        self.active_wave.spawn_enemies()

    def update(self, game_state: GameState, projectiles: [Projectile]) -> None:
        """Method to run on tick

        Spawns a new wave, if the current one is completed. Also updates all Enemies in the current wave.
        """
        if self.active_wave.is_complete:
            self.spawn_next_wave()
        self.active_wave.update(game_state, projectiles)

