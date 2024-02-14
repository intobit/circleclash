import pygame

from game.actors import Player
from game.utilities.gamestate import GameState

class Score:
    """Score Class"""

    def __init__(self, display: pygame.Surface):
        """Map Class"""
        self.display = display
        self.font = pygame.font.SysFont('comicsansms', 20)

    def draw(self, score: int) -> None:
        """
        Draws the score.

        :param score: score
        :return:
        """
        score_text = self.font.render(f'Score: {score}', True, (255, 255, 255))
        self.display.blit(score_text, (200, 1))

    def update(self, score: int, state: GameState) -> None:
        """
        Updates the map based on the Player.

        :param score: score
        :return:
        """
        if state is not GameState.READY:
            self.draw(score=score)

