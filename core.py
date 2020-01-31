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


class Game:
    def __init__(self, mode=constants.GAME_MODE, speed=constants.GAME_SPEED, gold_amount=constants.GOLD_AMOUNT):
        self.__mode = mode
        self.__action_frequency = constants.FPS / speed
        self.__init_gold_amount = self.gold_amount = gold_amount
        self.gnom = Gnom(constants.GNOM_X, constants.GNOM_Y)
        self.gold = helpers.initialize_all_gold(gold_amount, constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
        self.state = helpers.make_state(self.gnom, self.gold)
        self.step_counter = 0
        self.collected_gold = 0
        self.gnom_vision = helpers.make_gnom_vision(self.state, self.gnom.vision_size, self.gnom.x, self.gnom.y)

    def reset(self):
        self.gold_amount = self.__init_gold_amount
        self.gnom = Gnom(constants.GNOM_X, constants.GNOM_Y)
        self.gold = helpers.initialize_all_gold(self.gold_amount, constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
        self.state = helpers.make_state(self.gnom, self.gold)
        self.step_counter = 0
        self.collected_gold = 0
        self.gnom_vision = helpers.make_gnom_vision(self.state, self.gnom.vision_size, self.gnom.x, self.gnom.y)

    def get_gold(self):
        return self.collected_gold

    def get_map_gold(self):
        return self.gold

    def get_gnom(self):
        return self.gnom

    def get_state(self):
        return self.state

    def get_exit(self):
        return helpers.find_exit_distance(self.gnom)

    def remove_gold(self, gnom):
        for index, coin in enumerate(self.gold):
            if coin.x == gnom.x and coin.y == gnom.y:
                del self.gold[index]
                self.collected_gold += 1
                break

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

        # Check if gnom has stepped on a gold
        collect = helpers.check_coin_collect(self.gnom, self.gold)
        if collect:
            self.remove_gold(self.gnom)
        # Update state after moving gnom
        self.state = helpers.make_state(self.gnom, self.gold)
        self.gnom_vision = helpers.make_gnom_vision(self.state, self.gnom.vision_size, self.gnom.x, self.gnom.y)
        return self.gnom_vision

    def __initialize_game(self):
        pygame.init()
        pygame.display.set_caption("Gnom game by {}".format(self.__mode))
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

            action_taken = False

            # Build up a black screen as a game background
            screen.fill(constants.GAME_BACKGROUND)

            helpers.draw_game(screen, self.gnom, self.gnom_vision)

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
