import random
import constants


def make_empty_state(x_size, y_size):
    state = []
    for i in range(y_size):
        state_row = []
        for j in range(x_size):
            state_row.append(0)
        state.append(state_row)
    return state


def add_gnom(empty_state, gnom):
    empty_state[gnom.y][gnom.x] = 1
    return empty_state


def generate_random_gold_coords(x_cells, y_cells, x_reserved, y_reserved):
    x_coord = random.randrange(x_cells)
    y_coord = random.randrange(y_cells)
    while x_coord in x_reserved and y_coord in y_reserved:
        x_coord = random.randrange(x_cells)
        y_coord = random.randrange(y_cells)

    return x_coord, y_coord


def add_gold(state_with_gnom, gold):
    for coin in gold:
        state_with_gnom[coin.y][coin.x] = 2
    return state_with_gnom


def make_state(gnom, gold):
    # Building up an empty state to represent a map
    empty_state = make_empty_state(constants.CELL_AMOUNT_X, constants.CELL_AMOUNT_Y)
    # Adding gnom position on the map
    state_add_gnom = add_gnom(empty_state, gnom)
    # Adding all the coins of gold to the map
    state_add_gold = add_gold(state_add_gnom, gold)
    # Adding margin to the map based on the gnom's vision size
    margin_add_state = add_state_margin(state_add_gold, gnom.vision_size)
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


def make_gnom_vision(state, vision_size, x, y):
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

































