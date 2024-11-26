import pygame


class UI:
    def __init__(self, font_size=36):
        self.font = pygame.font.Font(None, font_size)

    def draw_score(self, screen, score):
        # Draw the current score on the screen
        score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
