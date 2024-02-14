from enum import Enum


class GameState(Enum):
    """Possible states of the game"""

    READY = 1
    """State before game has begun"""

    PAUSED = 2
    """State when game is paused"""

    RUNNING = 3
    """State while running the game"""

    WIN = 4
    """State when player has won"""

    GAME_OVER = 5
    """State when player has lost"""

    QUIT = 6
    """State when game should be quit"""
