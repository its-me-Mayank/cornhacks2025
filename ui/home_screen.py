import pygame
import random
import openai
import requests
from io import BytesIO
import time  # To add a delay for image generation
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT, OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.stage = "main"  # "main" -> first screen, "theme_select" -> theme input
        self.selected_theme = ""
        self.game_start = False
        self.theme_image = None
        self.storyline = ""
        self.waiting_for_image = False  # New flag to wait for image

        # Fonts
        self.title_font = pygame.font.Font(None, 80)  # Large font for "Hello"
        self.button_font = pygame.font.Font(None, 40)
        self.input_font = pygame.font.Font(None, 24)

        # Buttons
        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
        self.prompt_input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250, 300, 40)
        self.inspire_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 50)
        self.confirm_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)

        # User Input
        self.input_text = ""

    def draw_text(self, text, font, x, y, color=(255, 255, 255), max_width=500, max_lines=5):
        """Helper function to render text within a box with word wrapping and line limits."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
                if len(lines) >= max_lines:
                    break  # Stop adding lines when max_lines is reached

        lines.append(current_line)

        y_offset = 0
        for line in lines[:max_lines]:  # Only render up to max_lines
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + y_offset))
            y_offset += font.get_height()

    def run(self):
        """Draws the home screen UI, including text, buttons, AI-generated images, and storyline."""
        self.screen.fill((20, 20, 20))  # Dark background

        if self.stage == "main":
            # Show "Hello" text
            self.draw_text("Hello!", self.title_font, SCREEN_WIDTH // 2 - 100, 100, (255, 215, 0))

            # Start button
            pygame.draw.rect(self.screen, (100, 255, 100), self.start_button)
            self.draw_text("Start", self.button_font, SCREEN_WIDTH // 2 - 40, 315)

        elif self.stage == "theme_select":
            # Input box for custom theme
            pygame.draw.rect(self.screen, (50, 50, 50), self.prompt_input_box)
            self.draw_text(self.input_text, self.input_font, self.prompt_input_box.x + 10, self.prompt_input_box.y + 10)

            # "Inspire Me" button
            pygame.draw.rect(self.screen, (100, 100, 255), self.inspire_button)
            self.draw_text("Inspire Me", self.button_font, SCREEN_WIDTH // 2 - 70, 335)

            # Confirm button
            pygame.draw.rect(self.screen, (255, 100, 100), self.confirm_button)
            self.draw_text("Confirm", self.button_font, SCREEN_WIDTH // 2 - 50, 415)

            # Show loading text while waiting for AI image
            if self.waiting_for_image:
                self.draw_text("Generating image...", self.input_font, SCREEN_WIDTH // 2 - 80, 100, (255, 255, 255))
            elif self.theme_image:
                self.screen.blit(self.theme_image, (SCREEN_WIDTH // 2 - 128, 100))  # Adjusted position

            # Display AI-generated storyline inside a limited box
            if self.storyline:
                self.draw_text(self.storyline, self.input_font, 50, 450, (200, 200, 200), max_width=700, max_lines=5)

        self.handle_events()

    def handle_events(self):
        """Handles user interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.stage == "theme_select":
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, position):
        """Handles mouse clicks on buttons."""
        if self.stage == "main" and self.start_button.collidepoint(position):
            self.stage = "theme_select"
        elif self.stage == "theme_select":
            if self.inspire_button.collidepoint(position):
                self.selected_theme = self.generate_random_theme()
                self.storyline = self.generate_storyline(self.selected_theme)
                self.theme_image = None  # Reset image before generating a new one
                self.waiting_for_image = True  # Show "Generating image..." text
                pygame.display.flip()
                self.theme_image = self.generate_ai_image(self.selected_theme)
                self.waiting_for_image = False  # Remove "Generating image..." text
            elif self.confirm_button.collidepoint(position):
                self.start_game()

    def generate_random_theme(self):
        """Randomly selects a thematic pair for the game setting."""
        themes = [
            "Hero & Monster", "King & Queen", "Husband & Wife", "Detective & Criminal",
            "Knight & Dragon", "Alien & Astronaut", "Pirate & Treasure", "Time Traveler & Dinosaur",
            "Angel & Demon", "Robot & Human", "Spy & Hacker", "Cat & Mouse",
            "Scientist & Experiment", "Magician & Apprentice", "Doctor & Patient"
        ]
        return random.choice(themes)

    def generate_storyline(self, theme):
        """Uses AI to generate a short storyline based on the selected theme."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": f"Generate a short, engaging game storyline where players learn coding concepts. The theme is {theme}."}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"AI Storyline Error: {e}")
            return f"A thrilling adventure involving {theme}!"

    def generate_ai_image(self, theme):
        """Uses OpenAI API to generate an image based on the theme, with a lower quality option for faster loading."""
        try:
            response = openai.Image.create(
                prompt=f"A simple, cartoon-style image of {theme}.",
                n=1,
                size="128x128"  # Lower quality for faster loading
            )
            image_url = response["data"][0]["url"]

            # Download and convert the image for Pygame
            image_response = requests.get(image_url)
            image_data = BytesIO(image_response.content)
            return pygame.image.load(image_data)
        except Exception as e:
            print(f"AI Image Error: {e}")
            return None  # Return None if image generation fails

    def start_game(self):
        """Saves selected theme and moves to the game scene."""
        self.selected_theme = self.input_text if self.input_text else "Classic Pac-Man"
        self.game_start = True
