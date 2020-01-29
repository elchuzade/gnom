import constants
import helpers
import pygame


class Gold:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Gnom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vision_size = constants.GNOM_VISION_SIZE

    def move(self, direction):
        # Move the gnom in the given direction
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y -= 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y += 1


def initialize_all_gold(gold_amount, x_cells=constants.CELL_AMOUNT_X, y_cells=constants.CELL_AMOUNT_Y):
    used_x_coords = []
    used_y_coords = []
    all_gold = []
    for i in range(gold_amount):
        gold_x_coord, gold_y_coord = helpers.generate_random_gold_coords(x_cells, y_cells,
                                                                         used_x_coords, used_y_coords)
        gold = Gold(gold_x_coord, gold_y_coord)
        used_x_coords.append(gold_x_coord)
        used_y_coords.append(gold_y_coord)
        all_gold.append(gold)

    return all_gold


class Game:
    def __init__(self, gold_amount=constants.GOLD_AMOUNT):
        self.gold_amount = gold_amount
        self.gnom = Gnom(constants.GNOM_X, constants.GNOM_Y)
        self.gold = initialize_all_gold(self.gold_amount)
        self.state = helpers.make_state(self.gnom, self.gold)
        self.step_counter = 0
        self.gnom_vision = helpers.make_gnom_vision(self.state, self.gnom.vision_size, self.gnom.x, self.gnom.y)

    def get_gold(self):
        return self.gold

    def get_gnom(self):
        return self.gnom

    def get_state(self):
        return self.state

    def step(self, direction):
        # Move gnom in the given direction if not next ot the wall
        if direction == 0:
            # Check if there is a wall on the left by finding the center of the gnom's vision
            if self.gnom_vision[self.gnom.vision_size][self.gnom.vision_size - 1] != -1:
                self.gnom.move(0)

        elif direction == 1:
            # Check if there is a wall on the left by finding the center of the gnom's vision
            if self.gnom_vision[self.gnom.vision_size - 1][self.gnom.vision_size] != -1:
                self.gnom.move(1)

        elif direction == 2:
            # Check if there is a wall on the left by finding the center of the gnom's vision
            if self.gnom_vision[self.gnom.vision_size][self.gnom.vision_size + 1] != -1:
                self.gnom.move(2)

        elif direction == 3:
            # Check if there is a wall on the left by finding the center of the gnom's vision
            if self.gnom_vision[self.gnom.vision_size + 1][self.gnom.vision_size] != -1:
                self.gnom.move(3)

        # Update state after moving gnom
        self.state = helpers.make_state(self.gnom, self.gold)
        self.gnom_vision = helpers.make_gnom_vision(self.state, self.gnom.vision_size, self.gnom.x, self.gnom.y)
        return self.gnom_vision
