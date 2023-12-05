import pygame
import sys
from fsm import FSM

class Barbell:
    WIDTH = 300
    HEIGHT = 400
    OUTLINE_COLOR = (255, 0, 0)  # Red outline color

    def __init__(self, x, y, image_path):
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.outline_timer = 0  # Timer for the outline effect

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Draw the outline if the timer is active
        if self.outline_timer > 0:
            pygame.draw.rect(screen, self.OUTLINE_COLOR, self.rect, 2)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self):
        # Outline effect handling
        if self.outline_timer > 0:
            self.outline_timer -= 1  # Adjust the outline duration

    def start_outline_effect(self):
        self.outline_timer = 10  # Set the timer to initiate the outline effect

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clickable Image Counter")

        self.clock = pygame.time.Clock()

        self.counter = 0
        self.barbell = Barbell(50, self.height / 2 - 200, "final_project/assets/barbell.png")

        self.fsm = FSM()

    def run(self):
        font = pygame.font.Font(None, 36)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.barbell.is_clicked(event.pos):
                        self.increment_counter()
                        print(f"Counter value: {self.get_counter_value()}")
                        self.barbell.start_outline_effect()  # Trigger the outline effect

            self.barbell.update()  # Update the barbell's state

            self.screen.fill((255, 255, 255))

            # Draw the left section with the clickable image
            pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, self.width // 2, self.height))
            self.barbell.draw(self.screen)

            # Draw the right section (empty for now)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.width // 2, 0, self.width // 2, self.height))

            # Display the counter at the top of the screen
            counter_text = font.render(f"Counter: {self.get_counter_value()}", True, (0, 0, 0))
            self.screen.blit(counter_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

    def increment_counter(self):
        self.counter += 1

    def get_counter_value(self):
        return self.counter

if __name__ == "__main__":
    game = Game()
    game.run()
