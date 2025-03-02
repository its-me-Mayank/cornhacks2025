import random
import pygame
from scripts.settings import MAP_WIDTH, MAP_HEIGHT

class MapGenerator:
    def __init__(self, storyline):
        self.storyline = storyline
        self.map = self.generate_map()

        # Load images for the blocks
        self.outer_image = pygame.image.load("assets/blocks/outer.png")
        self.inner_image = pygame.image.load("assets/blocks/inner.png")
        self.obstacle_image = pygame.image.load("assets/blocks/obstacle.png")
        self.start_image = pygame.image.load("assets/blocks/start.png")
        self.goal_image = pygame.image.load("assets/blocks/goal.png")
        self.player_image = pygame.image.load("assets/blocks/player.png")

        # Resize images if necessary (optional but recommended to ensure uniform size)
        self.block_size = 32
        self.outer_image = pygame.transform.scale(self.outer_image, (self.block_size, self.block_size))
        self.inner_image = pygame.transform.scale(self.inner_image, (self.block_size, self.block_size))
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (self.block_size, self.block_size))
        self.start_image = pygame.transform.scale(self.start_image, (self.block_size, self.block_size))
        self.goal_image = pygame.transform.scale(self.goal_image, (self.block_size, self.block_size))
        self.player_image = pygame.transform.scale(self.player_image, (self.block_size, self.block_size))

    def generate_map(self):
        """Generate a map with more walkable paths and a goal."""
        # Create a grid (MAP_HEIGHT by MAP_WIDTH)
        grid = [['empty' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Create a path and place obstacles
        path = [(1, 1)]
        obstacles = []
        for y in range(2, MAP_HEIGHT - 2):  # Start filling in a clear path
            for x in range(2, MAP_WIDTH - 2):
                if random.random() > 0.2:  # 80% chance to add a path
                    path.append((x, y))
                else:
                    obstacles.append((x, y))  # Place obstacles in the other areas
        
        # Set start and goal
        start_position = (1, 1)
        goal_position = (MAP_WIDTH - 2, MAP_HEIGHT - 2)

        # Populate the grid with paths and obstacles
        for (x, y) in path:
            grid[y][x] = 'path'
        for (x, y) in obstacles:
            grid[y][x] = 'obstacle'
        
        grid[start_position[1]][start_position[0]] = 'start'
        grid[goal_position[1]][goal_position[0]] = 'goal'

        return grid

    def draw(self, screen):
        """Draw the map onto the screen."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                block_type = self.map[y][x]
                if block_type == 'path':
                    screen.blit(self.inner_image, (x * 32, y * 32))  # Draw a path block
                elif block_type == 'obstacle':
                    screen.blit(self.obstacle_image, (x * 32, y * 32))  # Draw an obstacle block
                elif block_type == 'start':
                    screen.blit(self.start_image, (x * 32, y * 32))  # Draw start
                elif block_type == 'goal':
                    screen.blit(self.goal_image, (x * 32, y * 32))  # Draw goal

    def convert_coordinates(self, coord):
        """Convert a coordinate to be used in the grid."""
        return tuple(map(int, coord))

    def get_start_position(self):
        """Return the starting position (where the player starts)."""
        return self.convert_coordinates(self.map[0][0])

    def get_goal_position(self):
        """Return the goal position (where the player should reach)."""
        return self.convert_coordinates(self.map[MAP_HEIGHT - 1][MAP_WIDTH - 1])
