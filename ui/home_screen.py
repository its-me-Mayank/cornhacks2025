import pygame
import openai
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT, OPENAI_API_KEY
from scripts.storyline_generator import generate_storyline

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.stage = "prompt"  # Stages: prompt -> storyline -> game
        self.user_prompt = ""
        self.storyline = ""
        self.game_start = False

        # Fonts
        self.title_font = pygame.font.Font(None, 60)
        self.button_font = pygame.font.Font(None, 35)
        self.input_font = pygame.font.Font(None, 28)

        # Buttons
        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
        self.next_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 60)

    def draw_text(self, text, font, x, y, color=(255, 255, 255), max_width=600):
        """Helper function to wrap text in a box."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + y_offset))
            y_offset += font.get_height()

    def run(self):
        """Draws the home screen UI with different stages."""
        self.screen.fill((20, 20, 20))

        if self.stage == "prompt":
            self.draw_text("Enter a Theme:", self.title_font, SCREEN_WIDTH // 2 - 150, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH // 2 - 150, 250, 300, 40))
            self.draw_text(self.user_prompt, self.input_font, SCREEN_WIDTH // 2 - 140, 260)

            pygame.draw.rect(self.screen, (100, 255, 100), self.start_button)
            self.draw_text("Start", self.button_font, SCREEN_WIDTH // 2 - 40, 315)

        elif self.stage == "storyline":
            self.draw_text("Storyline:", self.title_font, SCREEN_WIDTH // 2 - 100, 100)
            self.draw_text(self.storyline, self.input_font, 100, 200, max_width=600)

            pygame.draw.rect(self.screen, (255, 100, 100), self.next_button)
            self.draw_text("Next", self.button_font, SCREEN_WIDTH // 2 - 40, 460)

        self.handle_events()

    def handle_events(self):
        """Handles user interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.stage == "prompt":
                    if event.key == pygame.K_RETURN:
                        self.generate_story()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_prompt = self.user_prompt[:-1]
                    else:
                        self.user_prompt += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.stage == "prompt" and self.start_button.collidepoint(event.pos):
                    self.generate_story()
                elif self.stage == "storyline" and self.next_button.collidepoint(event.pos):
                    self.start_game()

    def generate_story(self):
        """Generate AI-based storyline from user input."""
        self.storyline = generate_storyline(self.user_prompt)
        self.stage = "storyline"

    def start_game(self):
        """Move to game stage."""
        self.game_start = True
