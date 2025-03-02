import pygame

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.game_start = False
        self.selected_theme = ""

        # UI Elements
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(200, 250, 400, 40)
        self.input_text = ""
        self.start_button = pygame.Rect(300, 400, 200, 50)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def run(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.input_box)
        pygame.draw.rect(self.screen, (100, 255, 100), self.start_button)

        self.draw_text("Enter Game Theme:", 260, 220)
        self.draw_text(self.input_text, 210, 260)
        self.draw_text("Start Game", 350, 415)

        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_game()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.start_game()

    def start_game(self):
        self.selected_theme = self.input_text if self.input_text else "Classic Pac-Man"
        self.game_start = True
