import pygame

# Stores the data for the different gyms           
class Gym:
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

    # Returns the player's income for a certain gym
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
    
    # Returns to the cost to buy a certain number of buildings
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
