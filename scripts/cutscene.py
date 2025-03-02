import pygame
import time

class Cutscene:
    def __init__(self, screen, theme):
        self.screen = screen
        self.theme = theme
        self.font = pygame.font.Font(None, 40)

    def show(self):
        """Displays a simple animated cutscene before the game starts."""
        self.screen.fill((0, 0, 0))  # Black background

        # Display story text
        text = f"A tale of {self.theme} begins..."
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (100, 250))

        # Simulate a simple animation (e.g., flashing text)
        pygame.display.flip()
        time.sleep(3)  # Pause for 3 seconds

        # Transition to the game after the cutscene
