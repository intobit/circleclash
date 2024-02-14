import pygame
from pygame.locals import *

from .utilities import GameState
from .utilities.events import *
from .actors import Player
from .ui import Map, Life, Settings, Score, Start, Win, Lose, WeaponBar, Wave_ui, UpperBar
from .waves import WaveManager
from .actors.enemy import Enemy
from .waves.generate_waves import generate_waves

# game settings
WINDOW_NAME = "Circle Clash"
BACKGROUND_MUSIC = "resources/sounds/Blade_Runner_Arcade_Music.mp3"

DEBUG_EVENT = pygame.USEREVENT + 100



class CircleClashGame:
    """Class containing the logic for the game

    This class manages all the individual components of the game, reacts to events and displays the UI. How it does that
    depends on the game's GameState (i.e., READY, RUNNING, WIN, GAME_OVER and PAUSED). It sets up all the necessary
    pygame objects, manages the game loop with all objects inside it, keeps track of the Player's score and updates
    the UI.
    """

    def __init__(self):
        """Class containing the logic for the game"""
        self._setup_pygame()
        self._set_initial_state()

        self.map = Map(display=self.display)
        self.life = Life(display=self.display)
        self.settings = Settings(display=self.display)
        self.scoreUI = Score(display=self.display)
        self.startUI = Start(display=self.display)
        self.winUI = Win(display=self.display)
        self.loseUI = Lose(display=self.display)
        self.weaponBar = WeaponBar(display=self.display, weapons=self.player.unlockable_weapons)
        self.wave_ui = Wave_ui(display=self.display)
        self.upperBar = UpperBar(display=self.display, height=33)

    def _setup_pygame(self) -> None:
        """Sets up pygame and the game window"""
        self.running = True
        pygame.init()
        self.clock = pygame.time.Clock()
        # self.display = pygame.display.set_mode((1024, 768))
        screen_info = pygame.display.Info()
        self.display = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption(WINDOW_NAME)
        pygame.mixer.init()
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.music_running = True

    def _toggle_music(self):
        if self.music_running:
            pygame.mixer.music.pause()
            self.music_running = False
        else:
            pygame.mixer.music.unpause()
            self.music_running = True

    def _set_initial_state(self) -> None:
        """Sets attributes related to the game's initial state"""
        self.score = 0
        self.state = GameState.READY
        self.player = Player(display=self.display)
        waves = generate_waves(self.display, self.player)
        self.waves = WaveManager(target=self.player, display=self.display, waves=waves)

    def _on_enemy_killed(self, enemy: Enemy) -> None:
        """Runs necessary actions when an enemy is killed"""
        self.score += enemy.points

    def _check_events(self) -> None:
        """Checks which events have been triggered"""

        def react_key_event(e: pygame.event.Event) -> None:
            """
            Reacts to keys being pressed

            Reacts to key events for buttons that are not held down but only shortly pressed.
            """
            if e.key == pygame.K_m:
                self._toggle_music()
            elif e.key == pygame.K_p:
                if self.state == GameState.RUNNING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.RUNNING

            elif e.key == pygame.K_SPACE and self.state in [
                GameState.GAME_OVER,
                GameState.WIN,
            ]:
                self.reset()
            elif e.key == pygame.K_i:
                self.waves.clear_current_wave()
                self.waves.spawn_next_wave()
            elif e.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

        for event in pygame.event.get():
            if event.type == QUIT:  # quit game on QUIT event
                self.running = False
            elif event.type == pygame.KEYDOWN:  # if a key is pressed, react to the corresponding event
                react_key_event(event)
            elif (
                # change game's state to GAME_OVER, when a PLAYER_KILLED_EVENT is received and the state isn't
                # GAME_OVER already.
                event.type == PLAYER_KILLED_EVENT and self.state != GameState.GAME_OVER
            ):
                self.state = GameState.GAME_OVER
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # on left click, attack with the Player or click on button
                    self.player.attack()
                    self.state = self.settings.toggleState(self.state)
                    self.state = self.startUI.toggleState(self.state)
                    self.state = self.winUI.toggleState(self.state)
                    self.state = self.loseUI.toggleState(self.state)
                    if self.state is None:
                        self.reset()
                    if self.state is GameState.QUIT:
                        self.running = False
            elif event.type == pygame.MOUSEWHEEL:
                # a MOUSEWHEEL event stores the wheel turn direction in y property as -1 (down) or 1 (up)
                # this is used to change the Player's 'active_weapon_idx'
                self.player.active_weapon_idx += event.y
            elif event.type == WIN_EVENT:
                # change the game's state to WIN, when a WIN_EVENT is received from the WaveManager
                self.state = GameState.WIN
            elif event.type == ENEMY_KILLED_EVENT:
                # react to an enemy being killed
                self._on_enemy_killed(event.killed)
            elif event.type == ENEMY_DESPAWN_EVENT:
                # despawn Enemies from the map when an ENEMY_DESPAWN_EVENT is received
                event.killed.kill()
            elif event.type == SPAWN_WAVE_EVENT:
                pass
            elif event.type == DEBUG_EVENT:
                # don't mind me, I'm just used for debugging
                if self.player.health <= 10:
                    self.player.health = 0
                else:
                    self.player.health *= 0.3

    def reset(self) -> None:
        """Resets the game

        Resets the Player, the WaveManager and the player's score.
        """
        self.player.reset()
        self.waves.clear_current_wave()
        self.score = 0
        self.state = GameState.RUNNING
        self.waves.reset()

    def run(self) -> None:
        """Main game loop"""
        # self.player.health = 0
        # pygame.time.set_timer(DEBUG_EVENT, 1_000, False)
        while self.running:
            self._check_events()
            self.map.update(player=self.player)
            self.upperBar.update(state=self.state)
            self.player.update(game_state=self.state, score=self.score)
            for enemy in self.waves.active_wave.spawned_enemies:
                if enemy.active_weapon is not None:
                    self.player.calc_new_health(projectiles=enemy.active_weapon.fired_projectiles)
            self.waves.update(game_state=self.state, projectiles=self.player.active_weapon.fired_projectiles)
            self.weaponBar.update(score=self.score)
            self.settings.update(state=self.state, score=self.score)
            self.startUI.update(state=self.state)
            self.winUI.update(state=self.state, score=self.score)
            self.loseUI.update(state=self.state, score=self.score)
            self.life.update(player=self.player, state=self.state)
            self.wave_ui.update(wave=self.waves.active_wave_index + 1, state=self.state)
            self.scoreUI.update(score=self.score, state=self.state)
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
