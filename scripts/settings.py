import os
# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40  # Each tile is 40x40 pixels

# Map Settings
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# OpenAI API Key (Replace with your own key)
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
