import pygame
import sys
from fsm import FSM
from gym import Gym
from barbell import Barbell

class Game:
    # Initialize the game
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clickable Image Counter")

        self.clock = pygame.time.Clock()

        self.counter = 0
        self.enemy_counter = 0
        self.enemy_increment = 10000000
        self.barbell = Barbell(50, 175, "assets/barbell.png")

        self.background = pygame.transform.scale(pygame.image.load("assets/Background.png"), (self.width, self.height))
        self.travel_background = pygame.transform.scale(pygame.image.load("assets/travel_screen.png"), (self.width, self.height))
        self.intro_background = pygame.transform.scale(pygame.image.load("assets/intro_background.png"), (self.width, self.height))
        self.win_screen = pygame.transform.scale(pygame.image.load("assets/Win_screen.png"), (self.width, self.height))
        self.train_more = pygame.transform.scale(pygame.image.load("assets/Train more.png"), (self.width, self.height))
        self.fsm = FSM()
        self.init_fsm()

        self.gyms = []
        self.gyms.append(Gym(["assets/weight.png", "assets/squat rack.png", "assets/bench.png", "assets/dumbell.png"],
                            [[0, 10, 1], [0, 1000, 10], [0, 100000, 100], [0, 10000000, 1000]]))
        self.gyms.append(Gym(["assets/hamstring_curl.png", "assets/leg_extension.png", "assets/leg_press.png", "assets/pec_dec.png"],
                             [[0, 1000, 10], [0, 50000, 600], [0, 20000000, 100000], [0, 99999999, 5000000]]))
        
        self.seconds_timer = 0  # Timer for tracking seconds

        # Button parameters
        self.button_width = 100
        self.button_height = 50
        self.button_color = (169, 169, 169)  # Pleasant grey button color

        self.buy_weight = pygame.Rect(490, 310, self.button_width, self.button_height)
        self.buy_squat = pygame.Rect(690, 310, self.button_width, self.button_height)
        self.buy_bench = pygame.Rect(490, 540, self.button_width, self.button_height)
        self.buy_dumbell = pygame.Rect(690, 540, self.button_width, self.button_height)
        self.buy_upgrade = pygame.Rect(600, 50, self.button_width, self.button_height)
        self.travel = pygame.Rect(400, 50, self.button_width, self.button_height)
        self.begin = pygame.Rect(400, 400, self.button_width, self.button_height)

    # Initialize the FSM
    def init_fsm(self) :
        for i in range(2) :
            self.fsm.add_transtition("to_travel", i, None, 'travel')
        self.fsm.add_transtition("to_first", "travel", None, 0)
        self.fsm.add_transtition("to_second", "travel", None, 1)
        self.fsm.add_transtition("challenge", "travel", None, "challenge")
        self.fsm.add_transtition("begin", "intro", None, 0)
        self.fsm.add_transtition("begin", "challenge", None, 0)
    
    # Game loop
    def run(self):
        self.font = pygame.font.Font(None, 36)
        while True:
            if (self.fsm.current_state == "intro") :
                self.intro()
            if (self.fsm.current_state == 0 or self.fsm.current_state == 1) :
                self.regular_mode(self.fsm.current_state)
            if (self.fsm.current_state == 'travel') :
                self.travel_mode()
            if (self.fsm.current_state == "challenge") :
                self.challenge_mode()
            self.seconds_timer += 1  # Increment the timer
            if self.seconds_timer == 60:  # Increment counter every 60 frames (1 second)
                self.increment_counter_by_money()
                self.seconds_timer = 0  # Reset the timer

    def increment_counter(self, number=1):
        self.counter += number

    def increment_counter_by_money(self):
        money_generated = self.calculate_money()
        self.counter += money_generated
        self.enemy_counter += self.enemy_increment

    def get_counter_value(self):
        return self.counter

    # Checks if player has the money for a building and purcahses it
    def purchase_building(self, building_type, number):
        cost = self.gym.get_cost(building_type, number)
        if self.get_counter_value() >= cost:
            self.increment_counter(-cost)  # Deduct the cost from the counter
            self.gym.purchase_building(building_type, number)

    # Checks if player can afford an upgrade and buys it
    def purchase_upgrade(self) :
        cost = self.gym.upgrade_cost
        if self.get_counter_value() >= cost:
            self.increment_counter(-cost)  # Deduct the cost from the counter
            self.gym.buy_upgrade()
            print("3")

    # Introduction state of the game
    def intro(self) :
        print("1")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.begin.collidepoint(event.pos) :
                    self.fsm.process("begin")

        self.screen.blit(self.intro_background, (0,0))
        
        pygame.draw.rect(self.screen, self.button_color, self.begin)
        button_text = self.font.render("Begin", True, (255, 255, 255))
        self.screen.blit(button_text, (400, 400))

        pygame.display.flip()
        self.clock.tick(60)
    
    # Regular mode of the game
    def regular_mode(self, current_gym):
        self.gym = self.gyms[current_gym]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.barbell.is_clicked(event.pos):
                    self.increment_counter()
                    print(f"Counter value: {self.get_counter_value()}")
                    self.barbell.start_outline_effect()  # Trigger the outline effect
                if self.buy_weight.collidepoint(event.pos) :
                    self.purchase_building(0, 1)
                if self.buy_squat.collidepoint(event.pos) :
                    self.purchase_building(1, 1)
                if self.buy_bench.collidepoint(event.pos) :
                    self.purchase_building(2, 1)
                if self.buy_dumbell.collidepoint(event.pos) :
                    self.purchase_building(3, 1)
                if self.buy_upgrade.collidepoint(event.pos):
                    self.purchase_upgrade()
                if self.travel.collidepoint(event.pos) :
                    self.fsm.process("to_travel")
                    return

        self.barbell.update()  # Update the barbell's state
        self.screen.blit(self.background, (0, 0))
        self.barbell.draw(self.screen)

        # Display the counter at the top of the screen
        counter_text = self.font.render(f"{self.get_counter_value()}", True, (0, 0, 0))
        self.screen.blit(counter_text, (110, 35))

        # Draw buttons and text onto the screen
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

        pygame.draw.rect(self.screen, self.button_color, self.travel)
        button_text = self.font.render("Travel", True, (255, 255, 255))
        self.screen.blit(button_text, (self.travel.topleft, self.travel.topright))

        # Display the building counters using the get_owned method
        weight_counter_text = self.font.render(f"{self.gym.get_owned(0)}", True, (0, 0, 0))
        self.screen.blit(weight_counter_text, (400, 145))

        squat_counter_text = self.font.render(f"{self.gym.get_owned(1)}", True, (0, 0, 0))
        self.screen.blit(squat_counter_text, (602, 145))

        bench_counter_text = self.font.render(f"{self.gym.get_owned(2)}", True, (0, 0, 0))
        self.screen.blit(bench_counter_text, (400, 380))

        dumbell_counter_text = self.font.render(f"{self.gym.get_owned(3)}", True, (0, 0, 0))
        self.screen.blit(dumbell_counter_text, (602, 380))

        enemy_counter_text = self.font.render(f"{self.enemy_counter}", True, (0, 0, 0))
        self.screen.blit(enemy_counter_text, (180, 90))

        pygame.draw.rect(self.screen, self.button_color, self.buy_upgrade)
        button_text = self.font.render(str(self.gym.get_upgrade_cost()), True, (255, 255, 255))
        self.screen.blit(button_text, (self.buy_upgrade.topleft, self.buy_upgrade.topright))

        # Draws the images for buildings that are owned
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

    # Travel screen
    def travel_mode(self) :
        gym_1 = pygame.Rect(125, 125, self.button_width, self.button_height)
        gym_2 = pygame.Rect(525, 125, self.button_width, self.button_height)
        challenge = pygame.Rect(490, 425, self.button_width, self.button_height)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gym_1.collidepoint(event.pos) :
                    self.fsm.process("to_first")
                    return
                if gym_2.collidepoint(event.pos) :
                    self.fsm.process("to_second")
                    return
                if challenge.collidepoint(event.pos) :
                    self.fsm.process("challenge")
                    return

        # Draw images and buttons
        self.screen.blit(self.travel_background, (0,0))

        pygame.draw.rect(self.screen, self.button_color, gym_1)
        button_text = self.font.render("Travel to Gym 1", True, (255, 255, 255))
        self.screen.blit(button_text, (gym_1.topleft, gym_1.topright))

        pygame.draw.rect(self.screen, self.button_color, gym_2)
        button_text = self.font.render("Travel to Gym 2", True, (255, 255, 255))
        self.screen.blit(button_text, (gym_2.topleft, gym_2.topright))

        pygame.draw.rect(self.screen, self.button_color, challenge)
        button_text = self.font.render("Challenge Arnold", True, (255, 255, 255))
        self.screen.blit(button_text, (challenge.topleft, challenge.topright))

        enemy_counter_text = self.font.render(f"{self.enemy_counter}", True, (0, 0, 0))
        self.screen.blit(enemy_counter_text, (280, 485))

        counter_text = self.font.render(f"{self.get_counter_value()}", True, (0, 0, 0))
        self.screen.blit(counter_text, (230, 405))

        pygame.display.flip()
        self.clock.tick(60)

    # Calculate total income
    def calculate_money(self) :
        money = 0
        for i in self.gyms :
            money += i.calculate_money()
        return money
    
    # Checks to see if the player has won the game
    def challenge_mode(self) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.begin.collidepoint(event.pos) :
                    self.fsm.process("begin")
    
        if (self.counter > self.enemy_counter) :
            self.screen.blit(self.win_screen, (0,0))
        else :
            self.screen.blit(self.train_more, (0,0))

            pygame.draw.rect(self.screen, self.button_color, self.begin)
            button_text = self.font.render("Begin", True, (255, 255, 255))
            self.screen.blit(button_text, (400, 400))

        pygame.display.flip()
        self.clock.tick(10)

# Scrapped
# class Enemy:
#     def __init__(self, maze) :
#         self.x = 6
#         self.y = 5
#         self.target = (6, 5)
#         self.path = []
#         self.maze = maze
#         self.image = pygame.transform.scale(pygame.image.load("assets/pixel_man.png"), (20, 20))

#     def move(self) :
#         if ((self.x, self.y) == self.target) :
#             self.target = self.maze.get_random_square()
#             self.get_path()
#         next_node = self.path.pop(0)
#         self.x = next_node[0]
#         self.y = next_node[1]

#     def get_path(self) :
#         self.get_path_dfs()

#     def get_path_dfs(self):
#         stack = []
#         parents = {}
#         visited = []

#         node = (self.x, self.y)
#         visited.append(node)
#         while (node != self.target) :
#             children = self.maze.find_children(node)
#             for child in children :
#                 if (child not in visited) :
#                     print("1")
#                     stack.append(child)
#                     visited.append(child)
#                     parents[child] = node
#             node = stack.pop()
#             print(node)
#             print(self.target)
#             print("_______")
    
#         node = self.target
#         self.path.insert(0, node)
#         while (node != (self.x, self.y)) :
#             self.path.insert(0, parents[node])
#             node = parents[node]

#     def draw(self, screen) :
#         screen.blit(self.image, (self.x * 20, self.y * 20))

# Scrapped this idea
# class Maze:
#     def __init__(self):
#         self.maze = []
#         self.wall = pygame.transform.scale(pygame.image.load("assets/brick.png"), (20, 20))
#         self.background = pygame.image.load("assets/end_background.png")
#         with open("assets/maze.txt") as file:
#             for line in file:
#                 self.maze.append(line.strip())  # Remove any trailing newline characters

#     def draw(self, screen):
#         # Assuming each block (wall or space) is of a fixed size
#         block_size = 20  # Adjust this size as needed

#         screen.blit(self.background, (0,0))
#         for y, row in enumerate(self.maze):
#             for x, char in enumerate(row):
#                 if char == '#':
#                     screen.blit(self.wall, (x * block_size, y * block_size))

    
#     def get_random_square(self) :
#         x = 0
#         y = 0
#         while self.maze[x][y] == "#" :
#             x = random.randint(0, 29)
#             y = random.randint(0, 30)
#         return (x, y)
    
#     def find_children(self, coords) :
#         children = []
#         if self.maze[coords[0] + 1][coords[1]] != '#' :
#             children.append((coords[0] + 1, coords[1]))
#         if self.maze[coords[0]][coords[1] + 1] != '#' :
#             children.append((coords[0], coords[1] + 1))
#         if self.maze[coords[0] - 1][coords[1]] != '#' :
#             children.append((coords[0] - 1, coords[1]))
#         if self.maze[coords[0]][coords[1] - 1] != '#' :
#             children.append((coords[0], coords[1] - 1))
#         return children
        
    

if __name__ == "__main__":
    game = Game()
    game.run()
