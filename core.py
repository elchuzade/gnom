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
        # Move the gnom in the given direction if not next ot the wall
        print(direction)


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

