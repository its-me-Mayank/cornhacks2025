import pygame
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT

TILE_SIZE = 40
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = (SCREEN_HEIGHT - 150) // TILE_SIZE  # Leave space for the terminal

class MapGenerator:
    def __init__(self, map_data):
        """Use AI-generated paths and obstacles."""
        self.start_position = map_data["start"]
        self.paths = set(map_data["paths"])
        self.obstacles = map_data["obstacles"]
        self.map = self.generate_map()

    def generate_map(self):
        """Creates a blank grid and fills it based on AI coordinates."""
        generated_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  # Default walls

        # Place paths
        for x, y in self.paths:
            generated_map[y][x] = 0  # 0 means walkable path

        # Place obstacles
        for x, y in self.obstacles:
            generated_map[y][x] = 2  # 2 represents obstacles

        return generated_map

    def draw(self, screen):
        """Draws the AI-generated map on screen."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.map[y][x] == 1:
                    pygame.draw.rect(screen, (100, 100, 100), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Walls
                elif self.map[y][x] == 0:
                    pygame.draw.rect(screen, (50, 50, 50), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Paths
                elif self.map[y][x] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Obstacles
