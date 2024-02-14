from os import path

import pygame
from game.utilities.helper_functions import read_image
from game.utilities import GameState


class Settings:
    """Settings Class"""

    def __init__(self, display: pygame.Surface):
        self.img = read_image(path.join("resources", "icons", "gear_bright.png"))
        self.img = pygame.transform.scale(self.img, (25, 25))
        self.display = display

        self.font = pygame.font.SysFont('comicsansms', 30)
        self.font_bigger = pygame.font.SysFont('comicsansms', 40)

        middle = ((self.display.get_width() // 2) - 85, (self.display.get_height() // 2))
        self.reset_cor = (middle[0], middle[1] + 70)
        self.cont_cor = (middle[0], middle[1])
        self.score_cor = (middle[0] - 100, middle[1] - 200)
        self.quit_cor = (middle[0], middle[1] + 140)

    def draw(self, state, score) -> None:
        if state is GameState.PAUSED:
            overlay = pygame.Surface(self.display.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(220)
            self.display.blit(overlay, (0, 0))

            text = self.font.render('Reset', True, (255, 255, 255))
            self.display.blit(text, self.reset_cor)

            text = self.font.render("Continue", True, (255, 255, 255))
            self.display.blit(text, self.cont_cor)

            text = self.font.render("Quit", True, (255, 0, 0))
            self.display.blit(text, self.quit_cor)

            text = self.font_bigger.render(f'YOUR SCORE: {score}', True, (255,255,255))
            self.display.blit(text, self.score_cor)

        self.display.blit(self.img, (self.display.get_width() - 30, 4))


    def toggleState(self, state) -> GameState or None:
        mouse = pygame.mouse.get_pos()
        if 970 + 20 > mouse[0] > 970 and 25 > mouse[1] > 2:
            if state == GameState.RUNNING:
                return GameState.PAUSED
            elif state == GameState.PAUSED:
                return GameState.RUNNING
        if state is GameState.PAUSED:
            if self.reset_cor[0] + 70 > mouse[0] > self.reset_cor[0] and self.reset_cor[1] + 40 > mouse[1] > self.reset_cor[1]:
                return None

            if self.cont_cor[0] + 95 > mouse[0] > self.cont_cor[0] and self.cont_cor[1] + 40 > mouse[1] > self.cont_cor[1]:
                return GameState.RUNNING

            if self.quit_cor[0] + 70 > mouse[0] > self.quit_cor[0] and self.quit_cor[1] + 40 > mouse[1] > self.quit_cor[1]:
                return GameState.QUIT

        return state

    def update(self, state, score):
        self.draw(state, score)

