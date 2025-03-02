import pygame
import time
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT

TILE_SIZE = 40
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE  # Map width to use all available horizontal space
MAP_HEIGHT = (SCREEN_HEIGHT - 150) // TILE_SIZE  # Map height, leaving space for the terminal

class MapGenerator:
    def __init__(self, map_data):
        """Generate the game map with expansive paths and obstacles."""
        self.start_position = self.convert_coordinates(map_data.get("start", (1, 1)))  # Default start position
        self.goal_position = self.convert_coordinates(map_data.get("goal", (MAP_WIDTH-2, MAP_HEIGHT-2)))  # Default goal position
        self.paths = [self.convert_coordinates(coord) for coord in map_data.get("paths", [(2, 1), (3, 1), (4, 1)])]  # Default paths
        self.obstacles = [self.convert_coordinates(coord) for coord in map_data.get("obstacles", [(3, 2), (5, 1)])]  # Default obstacles
        self.map = self.generate_map()
        self.character_position = self.start_position  # Character starts at the start position

    def convert_coordinates(self, coord):
        """Convert coordinates from string to integer tuple."""
        if isinstance(coord, str):
            coord = tuple(map(int, coord.strip("()").split(",")))  # Convert string tuple to actual tuple
        return coord

    def generate_map(self):
        """Creates an expansive map using all available space and wide paths."""
        generated_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  # Default walls

        # Mark the start position
        x, y = self.start_position
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            generated_map[y][x] = 3  # Mark the starting point with 3

        # Place two-tile wide paths
        for x, y in self.paths:
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                generated_map[y][x] = 0  # Mark path with 0 (walkable space)

        # Place obstacles in reasonable places
        for x, y in self.obstacles:
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                generated_map[y][x] = 2  # Mark obstacles with 2

        # Mark the goal position
        x, y = self.goal_position
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            generated_map[y][x] = 4  # Mark goal position with 4

        return generated_map

    def draw(self, screen):
        """Draw the map on the screen with different colors for paths, obstacles, and walls."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.map[y][x] == 1:
                    # Darker grey for walls (places you can't go)
                    pygame.draw.rect(screen, (30, 30, 30), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Walls
                elif self.map[y][x] == 0:
                    # Grey for paths (places you can go)
                    pygame.draw.rect(screen, (50, 50, 50), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Paths
                elif self.map[y][x] == 2:
                    # Red for obstacles (places you cannot pass)
                    pygame.draw.rect(screen, (255, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Obstacles
                elif self.map[y][x] == 3:
                    # Green for start (where the character starts)
                    pygame.draw.rect(screen, (0, 255, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Start (green)
                elif self.map[y][x] == 4:
                    # Yellow for goal (where the player needs to go)
                    pygame.draw.rect(screen, (255, 255, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Goal (yellow)

        # Draw the character (a blue ball)
        char_x, char_y = self.character_position
        pygame.draw.circle(screen, (0, 0, 255), (char_x * TILE_SIZE + TILE_SIZE // 2, char_y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

    def animate_character(self):
        """Animate the character moving from start to goal."""
        start_x, start_y = self.start_position
        goal_x, goal_y = self.goal_position

        # Animate the movement from start to goal
        while (start_x, start_y) != (goal_x, goal_y):
            if start_x < goal_x:
                start_x += 1
            elif start_x > goal_x:
                start_x -= 1
            if start_y < goal_y:
                start_y += 1
            elif start_y > goal_y:
                start_y -= 1

            self.character_position = (start_x, start_y)
            time.sleep(0.1)  # Slow down the movement to make it visible
