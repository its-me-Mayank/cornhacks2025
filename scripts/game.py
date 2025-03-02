import pygame
from scripts.ai_terminal import AITerminal
from scripts.map_generator import MapGenerator
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self, screen, theme):
        self.screen = screen
        self.theme = theme
        self.running = True

        # Initialize Map and AI Terminal
        self.map = MapGenerator()
        self.terminal = AITerminal("if-else")

    def run(self):
        """Main game loop"""
        while self.running:
            self.screen.fill((0, 0, 0))
            self.map.draw(self.screen)  # Draw the map
            self.handle_events()
            self.terminal.display(self.screen)  # Show coding challenge

            pygame.display.flip()
            pygame.time.delay(100)

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.terminal.handle_input(event)
