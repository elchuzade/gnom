import constants
import helpers
import pygame
import random
import numpy as np


class Model:
    """Creates an example of a deep learning model instance"""

    def __init__(self):
        self.placeholder = True

    def predict(self, state):
        action = random.randrange(4)
        return action


class Gold:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Gnome:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vision_size = constants.GNOM_VISION_SIZE

    def move(self, direction):
        # Move the gnome in the given direction
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y -= 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y += 1


class Game:
    def __init__(self, mode=constants.GAME_MODE, speed=constants.GAME_SPEED, gold_amount=constants.GOLD_AMOUNT):
        self.__mode = mode
        self.__action_frequency = constants.FPS / speed
        self.__init_gold_amount = self.gold_amount = gold_amount
        self.gnome = Gnome(constants.GNOM_X, constants.GNOM_Y)
        self.gold = helpers.initialize_all_gold(gold_amount, constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
        self.state = helpers.make_state(self.gnome, self.gold)
        self.step_counter = 0
        self.collected_gold = 0
        self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size, self.gnome.x, self.gnome.y)
        # 4 stands for collected_gold value, exit_distance value, gnome_x value and gnome_y value
        self.state_size = helpers.get_vision_size(self.gnome_vision) + 4
        self.model = Model()

    def soft_reset(self):
        self.gold_amount = self.__init_gold_amount
        self.gnome = Gnome(constants.GNOM_X, constants.GNOM_Y)
        self.gold = helpers.initialize_all_gold(self.gold_amount, constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
        self.state = helpers.make_state(self.gnome, self.gold)
        self.step_counter = 0
        self.collected_gold = 0
        self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size, self.gnome.x, self.gnome.y)
        # 4 stands for collected_gold value, exit_distance value, gnome_x value and gnome_y value
        self.state_size = helpers.get_vision_size(self.gnome_vision) + 4

    def reset(self):
        self.gold_amount = self.__init_gold_amount
        self.gnome = Gnome(constants.GNOM_X, constants.GNOM_Y)
        self.gold = helpers.initialize_all_gold(self.gold_amount, constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
        self.state = helpers.make_state(self.gnome, self.gold)
        self.step_counter = 0
        self.collected_gold = 0
        self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size, self.gnome.x, self.gnome.y)
        # 4 stands for collected_gold value, exit_distance value, gnome_x value and gnome_y value
        self.state_size = helpers.get_vision_size(self.gnome_vision) + 4
        self.model = Model()

    def get_gold(self):
        return self.collected_gold

    def get_map_gold(self):
        return self.gold

    def get_gnome_vision_flat(self):
        return helpers.flatten_gnome_vision(self.gnome_vision)

    def get_gnome_vision(self):
        return self.gnome_vision

    def get_gnome(self):
        return self.gnome

    def get_state(self):
        return self.state

    def get_exit(self):
        return helpers.find_exit_distance(self.gnome)

    def remove_gold(self, gnome):
        for index, coin in enumerate(self.gold):
            if coin.x == gnome.x and coin.y == gnome.y:
                del self.gold[index]
                self.collected_gold += 1
                break

    def step(self, direction):
        # Move gnome in the given direction if not next ot the wall
        if direction == 0:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.gnome_vision[self.gnome.vision_size][self.gnome.vision_size - 1] != -1:
                self.gnome.move(0)

        elif direction == 1:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.gnome_vision[self.gnome.vision_size - 1][self.gnome.vision_size] != -1:
                self.gnome.move(1)

        elif direction == 2:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.gnome_vision[self.gnome.vision_size][self.gnome.vision_size + 1] != -1:
                self.gnome.move(2)

        elif direction == 3:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.gnome_vision[self.gnome.vision_size + 1][self.gnome.vision_size] != -1:
                self.gnome.move(3)

        # Check if gnome has stepped on a gold
        collect = helpers.check_coin_collect(self.gnome, self.gold)
        if collect:
            self.remove_gold(self.gnome)
        # Update state after moving gnome
        self.state = helpers.make_state(self.gnome, self.gold)
        self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size, self.gnome.x, self.gnome.y)
        return self.gnome_vision

    def __initialize_game(self):
        pygame.init()
        pygame.display.set_caption("Gnome game by {}".format(self.__mode))
        size = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT
        screen = pygame.display.set_mode(size)
        font = pygame.font.Font(constants.FONT_NAME, constants.FONT_SIZE)

        # Clock is set to keep track of frames
        clock = pygame.time.Clock()
        pygame.display.flip()
        frame = 1
        action_taken = False
        while True:
            clock.tick(constants.FPS)
            pygame.event.pump()
            for event in pygame.event.get():
                if self.__mode == "player" and not action_taken:
                    # Look for any button press action
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            action_taken = True
                            action = 0  # 0 means go left
                            self.step(action)

                        elif event.key == pygame.K_UP:
                            action_taken = True
                            action = 1  # 1 means go up
                            self.step(action)

                        elif event.key == pygame.K_RIGHT:
                            action_taken = True
                            action = 2  # 2 means go right
                            self.step(action)

                        elif event.key == pygame.K_DOWN:
                            action_taken = True
                            action = 3  # 3 means go down
                            self.step(action)

                # Quit the game if the X symbol is clicked
                if event.type == pygame.QUIT:
                    print("pressing escape")
                    pygame.quit()
                    raise SystemExit

            if self.__mode == "ai":
                if frame % self.__action_frequency == 0:
                    self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size,
                                                                  self.gnome.x, self.gnome.y)

                    gnome_vision_flat = helpers.flatten_gnome_vision(self.gnome_vision)

                    gnome_vision_flat.extend([self.get_gold(), self.get_exit(), self.get_gnome().x, self.get_gnome().y])

                    reshaped_state = np.reshape(gnome_vision_flat, [1, self.state_size])
                    action = self.model.predict(reshaped_state)
                    self.gnome_vision = self.step(action)

                    done = helpers.check_if_exit(self.gnome)
                    if done:
                        self.soft_reset()

            action_taken = False

            # Build up a black screen as a game background
            screen.fill(constants.GAME_BACKGROUND)

            helpers.draw_game(screen, self.gnome, self.gnome_vision)

            gold_text_placeholder, gold_rect_text_placeholder = helpers.update_gold_text_placeholder(font)
            screen.blit(gold_text_placeholder, gold_rect_text_placeholder)

            exit_text_placeholder, exit_rect_text_placeholder = helpers.update_exit_text_placeholder(font)
            screen.blit(exit_text_placeholder, exit_rect_text_placeholder)

            gold_text, gold_text_rect = helpers.update_gold_text(font, self.get_gold())
            screen.blit(gold_text, gold_text_rect)

            exit_text, exit_text_rect = helpers.update_exit_text(font, self.get_exit())
            screen.blit(exit_text, exit_text_rect)

            # update display
            pygame.display.flip()
            frame += 1

    def play(self):
        if self.__mode == "ai":
            print("ai playing")
        self.__initialize_game()
