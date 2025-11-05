import random

from util import rand_between
from src.grid import Grid


def generate_majority_recolor(grid_size=(12, 12), block_num=(2, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    # randomize number of blocks for each color
    n1 = rand_between(*block_num)
    n2 = rand_between(block_num[0] - 1, n1 - 1) if n1 > 1 else 1

    color1, color2 = random.sample(colors, 2)

    # sample positions for both sets
    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    # fill input grid
    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    # fill output grid — everything becomes majority color
    for x, y in all_positions:
        grid_output.fill_cell(x, y, color1)

    return grid_input, grid_output


def generate_minority_recolor(grid_size=(12, 12), block_num=(2, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    # randomize number of blocks for each color
    n1 = rand_between(*block_num)
    n2 = rand_between(block_num[0] - 1, n1 - 1) if n1 > 1 else 1

    color1, color2 = random.sample(colors, 2)

    # sample positions for both sets
    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    # fill input grid
    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    # fill output grid — everything becomes minority color
    for x, y in all_positions:
        grid_output.fill_cell(x, y, color2)

    return grid_input, grid_output


def generate_inversion_recolor(grid_size=(12, 12), block_num=(1, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    # randomize number of blocks for each color
    n1 = rand_between(*block_num)
    n2 = rand_between(*block_num)

    color1, color2 = random.sample(colors, 2)

    # sample positions
    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    # fill input grid
    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    # fill output grid — invert colors
    for x, y in color1_positions:
        grid_output.fill_cell(x, y, color2)
    for x, y in color2_positions:
        grid_output.fill_cell(x, y, color1)

    return grid_input, grid_output


def generate_parity_recolor(grid_size=(12, 12), block_num=(1, 6), colors=("red", "blue")):
    """
    Places 1–6 random colored blocks (1x1 each).
    If the total number of blocks is odd → output = red,
    If even → output = blue.
    """
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = rand_between(*block_num)

    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n)

    # randomly assign colors (input can be mixed)
    for x, y in all_positions:
        grid_input.fill_cell(x, y, random.choice(colors))

    # determine parity
    if n % 2 == 1:  # odd
        output_color = colors[0]
    else:            # even
        output_color = colors[1]

    # recolor everything in output
    for x, y in all_positions:
        grid_output.fill_cell(x, y, output_color)

    return grid_input, grid_output
