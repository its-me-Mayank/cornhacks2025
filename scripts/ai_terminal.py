import pygame

class AITerminal:
    def __init__(self, concept):
        """AI Terminal for handling coding challenges based on the concept."""
        self.concept = concept
        self.input_text = ""
        self.active = True
        self.pre_filled_code = "def should_move_forward(obstacle):\n    # Fill in the missing if-else logic\n"

    def display(self, screen):
        """Display the terminal box."""
        pygame.draw.rect(screen, (50, 50, 50), (100, 450, 600, 100))  # Terminal Box
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f"Write a solution using {self.concept}:", True, (255, 255, 255))
        screen.blit(text_surface, (110, 460))

        # Display the pre-filled code
        pre_filled_surface = font.render(self.pre_filled_code, True, (200, 200, 200))
        screen.blit(pre_filled_surface, (110, 480))

        # Display user input
        user_code_surface = font.render(self.input_text, True, (255, 255, 255))
        screen.blit(user_code_surface, (110, 500))

    def handle_input(self, event):
        """Handle user input for coding."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.check_solution()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def check_solution(self):
        """Placeholder function to check the user's solution."""
        if "if" in self.input_text and "else" in self.input_text:
            print("✅ Correct! The character moves forward.")
        else:
            print("❌ Incorrect! Try again.")
