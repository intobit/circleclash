import pygame
from game.utilities import GameState


class Lose:
    """Lose Class"""

    def __init__(self, display: pygame.Surface):
        self.display = display

        self.font = pygame.font.SysFont('comicsansms', 30)
        self.font_bigger = pygame.font.SysFont('comicsansms', 40)

        middle = ((self.display.get_width() // 2) - 50, (self.display.get_height() // 2))
        self.reset_cor = (middle[0], middle[1])
        self.lose_cor = (middle[0] - 150, middle[1] - 250)
        self.score_cor = (middle[0] - 150, middle[1] - 200)
        self.quit_cor = (middle[0], middle[1] + 120)

    def draw(self, state, score) -> None:
        if state is GameState.GAME_OVER:
            overlay = pygame.Surface(self.display.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(220)
            self.display.blit(overlay, (0, 0))

            text = self.font_bigger.render('YOU LOST :( !!!', True, (255, 0, 0))
            self.display.blit(text, self.lose_cor)

            text = self.font.render("Reset", True, (255,255,255))
            self.display.blit(text, self.reset_cor)

            text = self.font.render("Quit", True, (255, 0, 0))
            self.display.blit(text, self.quit_cor)

            text = self.font_bigger.render(f'YOUR SCORE: {score}', True, (255,255,255))
            self.display.blit(text, self.score_cor)


    def toggleState(self, state) -> GameState or None:
        mouse = pygame.mouse.get_pos()

        if state is GameState.GAME_OVER:
            if self.reset_cor[0] + 70 > mouse[0] > self.reset_cor[0] and self.reset_cor[1] + 40 > mouse[1] > self.reset_cor[1]:
                return None

            if self.quit_cor[0] + 70 > mouse[0] > self.quit_cor[0] and self.quit_cor[1] + 40 > mouse[1] > self.quit_cor[1]:
                return GameState.QUIT

        return state

    def update(self, state, score):
        self.draw(state, score)

