import os
import pygame
import sys
from ui.home_screen import HomeScreen
from scripts.game import Game
from scripts.cutscene import Cutscene  # Ensures cutscene runs before the game

# Prevents Pygame audio errors in unsupported environments
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Initialize Pygame
pygame.init()

# Game Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI-Powered Learning Game")

def main():
    clock = pygame.time.Clock()

    # Start with Home Screen
    home_screen = HomeScreen(screen)
    game = None
    cutscene_played = False  # Ensure cutscene plays only once

    running = True
    while running:
        screen.fill((0, 0, 0))  # Black Background

        if home_screen.active:
            home_screen.run()
            if home_screen.game_start and not cutscene_played:
                # Show Cutscene Before Game Starts
                cutscene = Cutscene(screen, home_screen.selected_theme)
                cutscene.show()
                cutscene_played = True  # Mark cutscene as played

                # Start Game After Cutscene
                game = Game(screen, home_screen.selected_theme)
                home_screen.active = False
        elif game:
            game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
