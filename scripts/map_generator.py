import pygame
import random
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT

TILE_SIZE = 40  # Size of each tile
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = (SCREEN_HEIGHT - 150) // TILE_SIZE  # Leave space for the terminal

class MapGenerator:
    def __init__(self):
        self.map = self.generate_map()

    def generate_map(self):
        """Generates a simple grid-based map."""
        generated_map = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WIDTH):
                if random.random() < 0.1:  # Random walls (10% chance)
                    row.append(1)  # Wall
                else:
                    row.append(0)  # Path
            generated_map.append(row)

        # Ensure start and end positions are walkable
        generated_map[1][1] = 0  # Start position
        generated_map[MAP_HEIGHT - 2][MAP_WIDTH - 2] = 0  # End position
        return generated_map

    def draw(self, screen):
        """Draws the map on the screen."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.map[y][x] == 1:
                    pygame.draw.rect(screen, (100, 100, 100), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Walls
                else:
                    pygame.draw.rect(screen, (50, 50, 50), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Paths
