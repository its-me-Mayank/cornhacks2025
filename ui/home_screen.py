import pygame
from scripts.storyline_generator import generate_storyline, generate_map_from_story
from scripts.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.stage = "prompt"
        self.user_prompt = ""
        self.storyline = None
        self.map_data = {}  # Initialize map_data as an empty dictionary
        self.game_start = False

        # UI Elements
        self.title_font = pygame.font.Font(None, 60)
        self.button_font = pygame.font.Font(None, 35)
        self.input_font = pygame.font.Font(None, 28)

        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
        self.next_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 60)

    def draw_text(self, text, font, x, y, color=(255, 255, 255), max_width=600):
        """Helper function to render text with word wrapping."""
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
        """Handles the home screen UI based on the current stage."""
        self.screen.fill((20, 20, 20))

        if self.stage == "prompt":
            self.draw_text("Enter a Theme:", self.title_font, SCREEN_WIDTH // 2 - 150, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH // 2 - 150, 250, 300, 40))
            self.draw_text(self.user_prompt, self.input_font, SCREEN_WIDTH // 2 - 140, 260)

            pygame.draw.rect(self.screen, (100, 255, 100), self.start_button)
            self.draw_text("Start", self.button_font, SCREEN_WIDTH // 2 - 40, 315)

        elif self.stage == "waiting":
            self.draw_text("Generating Story...", self.title_font, SCREEN_WIDTH // 2 - 200, 250)

        elif self.stage == "storyline":
            self.draw_text("Storyline:", self.title_font, SCREEN_WIDTH // 2 - 100, 100)
            self.draw_text(self.storyline, self.input_font, 100, 200, max_width=600)

            pygame.draw.rect(self.screen, (255, 100, 100), self.next_button)
            self.draw_text("Next", self.button_font, SCREEN_WIDTH // 2 - 40, 460)

        elif self.stage == "map_generating":
            self.draw_text("Generating Map...", self.title_font, SCREEN_WIDTH // 2 - 200, 250)

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
                        self.start_story_generation()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_prompt = self.user_prompt[:-1]
                    else:
                        self.user_prompt += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.stage == "prompt" and self.start_button.collidepoint(event.pos):
                    self.start_story_generation()
                elif self.stage == "storyline" and self.next_button.collidepoint(event.pos):
                    self.start_map_generation()

    def start_story_generation(self):
        """Fetch AI-generated story first."""
        if self.storyline is None:
            self.stage = "waiting"
            generate_storyline(self.user_prompt, self.set_storyline)
        else:
            self.stage = "storyline"

    def set_storyline(self, story):
        """Receive AI-generated story."""
        self.storyline = story
        self.stage = "storyline"

    def start_map_generation(self):
        """After showing the story, generate the map."""
        self.stage = "map_generating"  # Show "Generating Map..." message
        generate_map_from_story(self.storyline, self.set_map_data)

    def set_map_data(self, map_data):
        """Receive AI-generated map data and transition to the game."""
        if map_data is None:
            print("AI map generation failed. Using default map.")
            map_data = {
                "start": (1, 1),
                "paths": [(2, 1), (3, 1), (4, 1)],
                "obstacles": [(3, 2), (5, 1)]
            }

        try:
            # Ensure the map data (start, goal, paths, obstacles) is properly formatted as tuples
            if isinstance(map_data.get("start"), tuple):
                self.map_data["start"] = map_data["start"]

            if isinstance(map_data.get("goal"), tuple):
                self.map_data["goal"] = map_data["goal"]

            if isinstance(map_data.get("paths"), list):
                # Ensure paths are in (x, y) tuple format
                self.map_data["paths"] = map_data["paths"]

            if isinstance(map_data.get("obstacles"), list):
                # Ensure obstacles are in (x, y) tuple format
                self.map_data["obstacles"] = map_data["obstacles"]

        except KeyError as e:
            print(f"KeyError: Missing data in map_data - {e}")
            return

        self.start_game()  # Directly move to game when map is ready

    def start_game(self):
        """Move to game stage."""
        self.game_start = True
