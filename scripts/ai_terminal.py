import pygame
import openai
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT, OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

class AITerminal:
    def __init__(self):
        self.active = False  # Terminal starts closed
        self.input_text = ""
        self.response_text = ""
        self.font = pygame.font.Font(None, 24)
        self.box = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)

    def toggle(self):
        """Opens or closes the terminal."""
        self.active = not self.active

    def handle_event(self, event):
        """Handles text input and submission."""
        if not self.active:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.process_code()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def process_code(self):
        """Sends pseudocode to AI for feedback and gets a response."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Check this pseudocode for errors and suggest improvements."},
                    {"role": "user", "content": self.input_text}
                ]
            )
            self.response_text = response["choices"][0]["message"]["content"]
        except Exception as e:
            self.response_text = f"AI Error: {e}"
        
        self.input_text = ""  # Clear input after processing

    def display(self, screen):
        """Displays the terminal box and text."""
        if not self.active:
            return

        pygame.draw.rect(screen, (30, 30, 30), self.box)  # Dark background
        pygame.draw.rect(screen, (200, 200, 200), self.box, 2)  # Border

        # Render input text
        input_surface = self.font.render(self.input_text, True, (255, 255, 255))
        screen.blit(input_surface, (self.box.x + 10, self.box.y + 10))

        # Render AI response
        response_surface = self.font.render(self.response_text, True, (150, 255, 150))
        screen.blit(response_surface, (self.box.x + 10, self.box.y + 50))
