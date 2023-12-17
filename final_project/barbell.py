import pygame

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
