import os
os.environ["SDL_AUDIODRIVER"] = "dummy"  # Prevents ALSA errors

import pygame
import sys
from ui.home_screen import HomeScreen
from scripts.game import Game


# Initialize Pygame
pygame.init()

# Game Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Pac-Man Learning Game")

# Main Function
def main():
    clock = pygame.time.Clock()
    
    # Start with Home Screen
    home_screen = HomeScreen(screen)
    game = None

    running = True
    while running:
        screen.fill((0, 0, 0))  # Black Background

        if home_screen.active:
            home_screen.run()
            if home_screen.game_start:
                # Load game with AI-generated theme
                game = Game(screen, home_screen.selected_theme)
                home_screen.active = False
        else:
            game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
