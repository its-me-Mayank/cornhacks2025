import random
import openai
from scripts.settings import MAP_WIDTH, MAP_HEIGHT, OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

class MapGenerator:
    def __init__(self, theme):
        self.theme = theme

    def generate_map(self):
        """Generates a simple 2D grid-based map based on the theme."""
        map_data = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]  # Default: Walls everywhere

        # AI can suggest patterns (if time allows)
        ai_suggestion = self.get_ai_map_suggestion()

        # Carve out a simple path for the player
        start_x, start_y = 1, 1
        map_data[start_y][start_x] = 0  # Open space
        for _ in range((MAP_WIDTH * MAP_HEIGHT) // 3):  # Create open paths
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            if direction == "UP" and start_y > 1:
                start_y -= 1
            elif direction == "DOWN" and start_y < MAP_HEIGHT - 2:
                start_y += 1
            elif direction == "LEFT" and start_x > 1:
                start_x -= 1
            elif direction == "RIGHT" and start_x < MAP_WIDTH - 2:
                start_x += 1
            map_data[start_y][start_x] = 0  # Mark as walkable path

        return map_data

    def get_ai_map_suggestion(self):
        """Uses OpenAI to generate a custom map pattern based on the theme."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": f"Generate a simple 2D map pattern for a Pac-Man style game with theme: {self.theme}"}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"AI Error: {e}")
            return "Default maze layout"

