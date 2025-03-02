import pygame
import random
from scripts.map_generator import MapGenerator
from scripts.ai_terminal import AITerminal
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class Game:
    def __init__(self, screen, theme):
        self.screen = screen
        self.running = True
        self.theme = theme

        # Load AI-generated map
        self.map_generator = MapGenerator(theme)
        self.map_data = self.map_generator.generate_map()

        # Player Settings
        self.player_x, self.player_y = 1, 1  # Starting position
        self.player_color = (255, 255, 0)  # Pac-Man color
        self.speed = TILE_SIZE

        # AI Terminal
        self.terminal = AITerminal()

    def run(self):
        """Main game loop"""
        while self.running:
            self.screen.fill((0, 0, 0))  # Black background
            self.handle_events()
            self.draw_map()
            self.draw_player()
            self.terminal.display(self.screen)

            pygame.display.flip()
            pygame.time.delay(100)

    def handle_events(self):
        """Handle key events for movement"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.can_move(self.player_x - 1, self.player_y):
            self.player_x -= 1
        if keys[pygame.K_RIGHT] and self.can_move(self.player_x + 1, self.player_y):
            self.player_x += 1
        if keys[pygame.K_UP] and self.can_move(self.player_x, self.player_y - 1):
            self.player_y -= 1
        if keys[pygame.K_DOWN] and self.can_move(self.player_x, self.player_y + 1):
            self.player_y += 1

    def can_move(self, x, y):
        """Check if player can move to the given position"""
        return self.map_data[y][x] == 0  # 0 means open space

    def draw_map(self):
        """Draws the game map"""
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 1:  # Walls
                    pygame.draw.rect(
                        self.screen, (0, 0, 255),  # Blue walls
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

    def draw_player(self):
        """Draws the player character"""
        pygame.draw.circle(
            self.screen, self.player_color,
            (self.player_x * TILE_SIZE + TILE_SIZE // 2, self.player_y * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2
        )
