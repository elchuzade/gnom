import random
import constants
import core
import pygame


def make_empty_state(x_size, y_size):
    state = []
    for i in range(y_size):
        state_row = []
        for j in range(x_size):
            state_row.append(0)
        state.append(state_row)
    return state


def add_gnome(empty_state, gnome):
    empty_state[gnome.y][gnome.x] = 1
    return empty_state


def initialize_all_gold(gold_amount, x_cells=constants.CELL_AMOUNT_X, y_cells=constants.CELL_AMOUNT_Y):
    all_gold = []
    possible_coords = []
    for i in range(y_cells):
        for j in range(x_cells):
            # Exclude Gnome and Exit coordinates from the possible_coords x and y to not make coin on top of them
            if (j != constants.GNOME_X or i != constants.GNOME_Y) and (j != constants.EXIT_X or i != constants.EXIT_Y):
                possible_coords.append({
                    "x": j,
                    "y": i
                })

    for i in range(gold_amount):
        random_index = random.randrange(len(possible_coords))
        random_coords = possible_coords.pop(random_index)
        gold_x_coord, gold_y_coord = random_coords["x"], random_coords["y"]
        gold = core.Gold(gold_x_coord, gold_y_coord)
        all_gold.append(gold)

    return all_gold


def check_if_exit(gnome):
    if gnome.x == constants.EXIT_X and gnome.y == constants.EXIT_Y:
        return True
    return False


def add_gold(state_with_gnome, gold):
    for coin in gold:
        state_with_gnome[coin.y][coin.x] = 2
    return state_with_gnome


def make_state(gnome, gold):
    # Building up an empty state to represent a map
    empty_state = make_empty_state(constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
    # Adding gnome position on the map
    state_add_gnome = add_gnome(empty_state, gnome)
    # Add exit gate to the map
    state_add_exit = add_exit(state_add_gnome)
    # Adding all the coins of gold to the map
    state_add_gold = add_gold(state_add_exit, gold)
    # Adding margin to the map based on the gnome's vision size
    margin_add_state = add_state_margin(state_add_gold, gnome.vision_size)
    return margin_add_state


def add_state_margin(state, vision_size):
    margin_state = []
    margin_row = []

    # Build up a placeholder for the horizontal margin walls
    for i in range(len(state[0]) + vision_size * 2):
        # -1 represents walls ie non accessible cells
        margin_row.append(-1)

    # Add top margin
    for i in range(vision_size):
        margin_state.append(margin_row)

    for row in state:
        mid_line = []
        # Adding first vision_size amount of -1s to the beginning of the row
        for i in range(vision_size):
            mid_line.append(-1)

        # Adding the actual row to the mid_line
        mid_line.extend(row)

        # Adding last vision_size amount of -1s to the end of the row
        for i in range(vision_size):
            mid_line.append(-1)

        # Adding built up row to the actual state
        margin_state.append(mid_line)

    # Add bottom margin
    for i in range(vision_size):
        margin_state.append(margin_row)

    return margin_state


def make_gnome_vision(state, vision_size, x, y):
    x_vis = x + vision_size
    y_vis = y + vision_size

    vision = []

    # 2 * vision_size + 1 -> Because vision_size is a distance form your front to the furthers cell
    for row in range(2 * vision_size + 1):
        vision_row = []

        for col in range(2 * vision_size + 1):
            cell = state[y_vis + row - vision_size][x_vis + col - vision_size]
            vision_row.append(cell)

        vision.append(vision_row)

    return vision


def add_exit(state):
    # Place the exit gate to the right side in the middle
    state[len(state) // 2][-1] = 9
    return state


def get_vision_size(vision):
    count = 0
    for vision_row in vision:
        count += len(vision_row)
    return count


def flatten_gnome_vision(vision):
    flat_vision = []
    for vision_row in vision:
        flat_vision.extend(vision_row)
    return flat_vision


def find_exit_distance(gnome):
    return abs(constants.EXIT_Y - gnome.y) + abs(constants.EXIT_X - gnome.x)


def check_coin_collect(gnome, gold):
    for coin in gold:
        if coin.x == gnome.x and coin.y == gnome.y:
            return True
    return False


def update_gold_text_placeholder(font):
    text = font.render("GOLD: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 - constants.TEXT_WIDTH * 2,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_exit_text_placeholder(font):
    text = font.render("EXIT: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 + constants.TEXT_WIDTH,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_gold_text(font, collected_gold):
    text = font.render(str(collected_gold), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 - constants.TEXT_WIDTH,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_exit_text(font, exit_distance):
    text = font.render(str(exit_distance), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 + constants.TEXT_WIDTH * 2,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


"""DRAW STUFF"""


def draw_scoreboard(screen):
    pygame.draw.rect(screen, constants.SCOREBOARD_BACKGROUND, (0, constants.GAME_PLAY_HEIGHT + constants.MARGIN * 2,
                                                               constants.GAME_PLAY_WIDTH + constants.MARGIN * 2,
                                                               constants.SCOREBOARD_HEIGHT))


def draw_margins(screen):
    # Left line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN,
                                                           constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Right line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND,
                     (constants.MARGIN + constants.GAME_PLAY_WIDTH, constants.MARGIN,
                      constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Top line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, 0,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))
    # Bottom line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN + constants.GAME_PLAY_HEIGHT,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))


def draw_grid(screen):
    # Draws a grid to separate each game cell
    for i in range(constants.CELL_AMOUNT_X - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.MARGIN,
                                                             constants.GRID_LINE_WIDTH,
                                                             constants.CELL_SIZE * constants.CELL_AMOUNT_Y))

    for i in range(constants.CELL_AMOUNT_Y - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN,
                                                             constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.CELL_SIZE * constants.CELL_AMOUNT_X,
                                                             constants.GRID_LINE_WIDTH))


def draw_gnome(screen, gnome):
    pygame.draw.circle(screen, constants.GNOME_COLOR,
                       [int(gnome.x * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN,
                        int(gnome.y * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN],
                       int(constants.GNOME_RADIUS))


def draw_gold(screen, gnome, vision_size, row, col):
    pygame.draw.circle(screen, constants.GOLD_COLOR,
                       [int((gnome.x + col - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                        constants.MARGIN,
                        int((gnome.y + row - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                        constants.MARGIN],
                       int(constants.GOLD_RADIUS))


def draw_vision_cell(screen, gnome, vision_size, row, col):
    pygame.draw.rect(screen, constants.GNOME_VISION_COLOR,
                     ((col + gnome.x - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                      (row + gnome.y - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                      constants.CELL_SIZE, constants.CELL_SIZE))


def draw_vision(screen, gnome, vision):
    for row in range(len(vision)):
        for col in range(len(vision[row])):
            draw_vision_cell(screen, gnome, len(vision[0]) // 2, row, col)
            if vision[row][col] == 2:
                draw_gold(screen, gnome, len(vision[0]) // 2, row, col)


def draw_exit(screen):
    pygame.draw.rect(screen, constants.EXIT_COLOR, (constants.EXIT_X * constants.CELL_SIZE + constants.MARGIN,
                                                    constants.EXIT_Y * constants.CELL_SIZE + constants.MARGIN,
                                                    constants.CELL_SIZE, constants.CELL_SIZE))


def draw_game(screen, gnome, vision):
    draw_vision(screen, gnome, vision)
    draw_margins(screen)
    draw_scoreboard(screen)
    draw_grid(screen)
    draw_exit(screen)
    draw_gnome(screen, gnome)
