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
        self.barbell = Barbell(50, 175, "assets/barbell.png")

        self.background = pygame.transform.scale(pygame.image.load("assets/Background.png"), (self.width, self.height))
        self.fsm = FSM()

        self.gym = gym_1()
        self.seconds_timer = 0  # Timer for tracking seconds

        # Button parameters
        self.button_width = 100
        self.button_height = 50
        self.button_color = (169, 169, 169)  # Pleasant grey button color

        self.buy_weight = pygame.Rect(490, 310,
                                       self.button_width, self.button_height)
        self.buy_squat = pygame.Rect(690, 310,
                                       self.button_width, self.button_height)
        self.buy_bench = pygame.Rect(490, 540,
                                       self.button_width, self.button_height)
        
        self.buy_dumbell = pygame.Rect(690, 540, self.button_width, self.button_height)

        self.buy_upgrade = pygame.Rect(600, 50, self.button_width, self.button_height)
        

    def run(self):
        self.font = pygame.font.Font(None, 36)
        while True:
            self.regular_mode()
            self.seconds_timer += 1  # Increment the timer
            if self.seconds_timer == 60:  # Increment counter every 60 frames (1 second)
                self.increment_counter_by_money()
                self.seconds_timer = 0  # Reset the timer

    def increment_counter(self, number=1):
        self.counter += number

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
            print("2")

    def purchase_upgrade(self) :
        cost = self.gym.upgrade_cost
        if self.get_counter_value() >= cost:
            self.increment_counter(-cost)  # Deduct the cost from the counter
            self.gym.buy_upgrade()
            print("3")
    
    def regular_mode(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.barbell.is_clicked(event.pos):
                    self.increment_counter()
                    print(f"Counter value: {self.get_counter_value()}")
                    self.barbell.start_outline_effect()  # Trigger the outline effect
                if self.buy_weight.collidepoint(event.pos):
                    self.purchase_building(0, 1)
                    print('1')
                if self.buy_squat.collidepoint(event.pos):
                    self.purchase_building(1, 1)
                    print('2')
                if self.buy_bench.collidepoint(event.pos):
                    self.purchase_building(2, 1)
                    print('3')
                if self.buy_upgrade.collidepoint(event.pos):
                    self.purchase_upgrade()
                    print("up")

        self.barbell.update()  # Update the barbell's state

        self.screen.blit(self.background, (0, 0))

        
        self.barbell.draw(self.screen)

        # Display the counter at the top of the screen
        counter_text = self.font.render(f"{self.get_counter_value()}", True, (0, 0, 0))
        self.screen.blit(counter_text, (110, 35))

        # Draw the button on the right side of the screen
        pygame.draw.rect(self.screen, self.button_color, self.buy_weight)
        button_text = self.font.render(str(self.gym.buildings[0][1]), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_weight.topleft, self.buy_weight.topright))

        pygame.draw.rect(self.screen, self.button_color, self.buy_squat)
        button_text = self.font.render(str(self.gym.buildings[1][1]), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_squat.topleft, self.buy_squat.topright))

        pygame.draw.rect(self.screen, self.button_color, self.buy_bench)
        button_text = self.font.render(str(self.gym.buildings[2][1]), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_bench.topleft, self.buy_bench.topright))

        pygame.draw.rect(self.screen, self.button_color, self.buy_dumbell)
        button_text = self.font.render(str(self.gym.buildings[3][1]), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_dumbell.topleft, self.buy_dumbell.topright))

        # Display the building counters using the get_owned method
        weight_counter_text = self.font.render(f"{self.gym.get_owned(0)}", True, (0, 0, 0))
        self.screen.blit(weight_counter_text, (400, 145))

        squat_counter_text = self.font.render(f"{self.gym.get_owned(1)}", True, (0, 0, 0))
        self.screen.blit(squat_counter_text, (602, 145))

        bench_counter_text = self.font.render(f"{self.gym.get_owned(2)}", True, (0, 0, 0))
        self.screen.blit(bench_counter_text, (400, 380))

        dumbell_counter_text = self.font.render(f"{self.gym.get_owned(3)}", True, (0, 0, 0))
        self.screen.blit(dumbell_counter_text, (602, 380))

        pygame.draw.rect(self.screen, self.button_color, self.buy_upgrade)
        button_text = self.font.render(str(self.gym.get_upgrade_cost()), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_upgrade.topleft, self.buy_upgrade.topright))

        if (self.gym.buildings[0][0] != 0) :
            self.screen.blit(self.gym.images[0], (400, 145))
        if (self.gym.buildings[1][0] != 0) :
            self.screen.blit(self.gym.images[1], (600, 145))
        if (self.gym.buildings[2][0] != 0) :
            self.screen.blit(self.gym.images[2], (400, 370))
        if (self.gym.buildings[3][0] != 0) :
            self.screen.blit(self.gym.images[3], (600, 370))


        pygame.display.flip()
        self.clock.tick(60)

class button:
    def __init__(self, x, y, width, height):
        self.buy_weight = pygame.Rect(x, y, width, height)
    
    def change_function(self, method) :
        self.method = method


        
# Make it a list of gyms that each have different instance variables
class gym_1:
    def __init__(self) :
        self.images = []
        image_paths = ["assets/weight.png", "assets/squat rack.png", "assets/bench.png", "assets/dumbell.png"]

        for path in image_paths:
            original_image = pygame.image.load(path)
            scaled_image = pygame.transform.scale(original_image, (200, 200))
            self.images.append(scaled_image)
        # self.images[3] = pygame.image.load("assets/weight.png")

        # [Amount of building, initial price of building, strength generated per second]
        self.buildings = []
        self.buildings.append([0, 10, 1])
        self.buildings.append([0, 1000, 10])
        self.buildings.append([0, 100000, 100])
        self.buildings.append([0, 10000000, 1000])

        self.upgrades = 0
        self.upgrade_cost = 10

    def calculate_money(self) :
        money = 0
        for i in self.buildings:
            money += (i[0] * i[2])
        return money * (2 ** self.upgrades)
    
    def get_upgrade_cost(self) :
        return self.upgrade_cost
    
    def buy_upgrade(self) :
        self.upgrades += 1
        self.upgrade_cost *= 10
    
    def get_cost(self, building, number) :
        sum = 0
        cost = self.buildings[building][1]
        for i in range(number) :
            sum = int(sum + cost)
            cost *= 1.1
        return self.buildings[building][1] * number

    def purchase_building(self, building, number) :
        self.buildings[building][0] += number
        self.buildings[building][1] = int(self.buildings[building][1] * 1.1)

    def get_owned(self, building) :
        return self.buildings[building][0]

class gym:
    def __init__(self, image_paths, buildings) :
        self.images = []

        for path in image_paths:
            original_image = pygame.image.load(path)
            scaled_image = pygame.transform.scale(original_image, (200, 200))
            self.images.append(scaled_image)

        # [Amount of building, initial price of building, strength generated per second]
        self.buildings = buildings
        self.upgrades = 0
        self.upgrade_cost = 10

    def calculate_money(self) :
        money = 0
        for i in self.buildings:
            money += (i[0] * i[2])
        return money * (2 ** self.upgrades)
    
    def get_upgrade_cost(self) :
        return self.upgrade_cost
    
    def buy_upgrade(self) :
        self.upgrades += 1
        self.upgrade_cost *= 10
    
    def get_cost(self, building, number) :
        sum = 0
        cost = self.buildings[building][1]
        for i in range(number) :
            sum = int(sum + cost)
            cost *= 1.1
        return self.buildings[building][1] * number

    def purchase_building(self, building, number) :
        self.buildings[building][0] += number
        self.buildings[building][1] = int(self.buildings[building][1] * 1.1)

    def get_owned(self, building) :
        return self.buildings[building][0]

if __name__ == "__main__":
    game = Game()
    game.run()
