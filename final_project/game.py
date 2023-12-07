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
        self.barbell = Barbell(50, self.height / 2 - 200, "assets/barbell.png")

        self.fsm = FSM()

        self.gym = gym_1()
        self.seconds_timer = 0  # Timer for tracking seconds

        # Button parameters
        self.button_width = 100
        self.button_height = 50
        self.button_color = (0, 255, 0)  # Green button color
        self.button_rect = pygame.Rect(self.width - self.button_width, self.height / 2 - self.button_height / 2,
                                       self.button_width, self.button_height)

    def run(self):
        self.font = pygame.font.Font(None, 36)
        while True:
            self.regular_mode()
            self.seconds_timer += 1  # Increment the timer
            if self.seconds_timer == 60:  # Increment counter every 60 frames (1 second)
                self.increment_counter_by_money()
                self.seconds_timer = 0  # Reset the timer

    def increment_counter(self):
        self.counter += 1

    def increment_counter_by_money(self):
        money_generated = self.gym.calculate_money()
        self.counter += money_generated
        print(f"Counter value: {self.get_counter_value()} (+{money_generated} money)")


    def get_counter_value(self):
        return self.counter
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.button_rect.collidepoint(event.pos):
                        self.purchase_building(0, 1)
                        print('1')

    def purchase_building(self, building_type, number):
        cost = self.gym.get_cost(building_type, number)
        if self.get_counter_value() >= cost:
            self.increment_counter(-cost)  # Deduct the cost from the counter
            self.gym.purchase_building(building_type, number)
    
    def regular_mode(self):
        # state = self.fsm.get_state()

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
        counter_text = self.font.render(f"Counter: {self.get_counter_value()}", True, (0, 0, 0))
        self.screen.blit(counter_text, (10, 10))

        # Draw the button on the right side of the screen
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        button_text = self.font.render("Add Building", True, (255, 255, 255))
        self.screen.blit(button_text, (self.width - self.button_width + 10, self.height / 2 - self.button_height / 2 + 10))

        pygame.display.flip()
        self.clock.tick(60)

        

class gym_1:
    def __init__(self) :
        self.images = []
        self.images.append(pygame.image.load("assets/weight.png"))
        self.images.append(pygame.image.load("assets/squat rack.png"))
        self.images.append(pygame.image.load("assets/bench.png"))
        # self.images[3] = pygame.image.load("assets/weight.png")

        # [Amount of building, initial price of building, strength generated per second]
        self.buildings = []
        self.buildings.append([0, 100, 10])
        self.buildings.append([0, 1000, 100])
        self.buildings.append([0, 100000, 1000])
        self.buildings.append([0, 10000000, 10000])

    def calculate_money(self) :
        money = 0
        for i in self.buildings:
            money += (i[0] * i[2])
        return money
    
    def get_cost(self, building, number) :
        return self.buildings[building][1] * number

    def purchase_building(self, building, number) :
        self.buildings[building][2] += number

if __name__ == "__main__":
    game = Game()
    game.run()
