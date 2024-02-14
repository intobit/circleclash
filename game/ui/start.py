import pygame
from game.utilities import GameState


class Start:
    """StartScreen Class"""

    def __init__(self, display: pygame.Surface):
        self.display = display

        self.font = pygame.font.SysFont('comicsansms', 30)
        self.font_bigger = pygame.font.SysFont('comicsansms', 40)
        self.font_smaller = pygame.font.SysFont('comicsansms', 10)

        middle = ((self.display.get_width() // 2) - 50, (self.display.get_height() // 2))
        self.start_cor = (middle[0], middle[1])
        self.welcome_cor = (middle[0] - 180, middle[1] - 200)
        self.quit_cor = (middle[0], middle[1] + 120)
        self.names_cor = (5, self.display.get_height() - 30)


    def draw(self, state) -> None:
        if state is GameState.READY:
            overlay = pygame.Surface(self.display.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(220)
            self.display.blit(overlay, (0, 0))

            text = self.font.render('Start', True, (0, 255, 0))
            self.display.blit(text, self.start_cor)

            text = self.font.render('Quit', True, (255, 0, 0))
            self.display.blit(text, self.quit_cor)

            text = self.font_bigger.render('Welcome to Circle Clash', True, (255,255,30))
            self.display.blit(text, self.welcome_cor)

            text = self.font_smaller.render('Arbesser, Aldrian, Bartholomäus, Deutsch, Höck, Hirsch', True, (255,255,255))
            self.display.blit(text, self.names_cor)

    def toggleState(self, state) -> GameState:
        if state is GameState.READY:
            mouse = pygame.mouse.get_pos()
            if self.start_cor[0] + 90 > mouse[0] > self.start_cor[0] and self.start_cor[1] + 40 > mouse[1] > self.start_cor[1]:
                return GameState.RUNNING

            if self.quit_cor[0] + 70 > mouse[0] > self.quit_cor[0] and self.quit_cor[1] + 40 > mouse[1] > self.quit_cor[1]:
                return GameState.QUIT

        return state

    def update(self, state):
        self.draw(state)

