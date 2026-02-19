import random
from src.util import rand_between
from src.grid import Grid


def generate_majority_recolor(grid_size=(12, 12), block_num=(2, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n1 = rand_between(*block_num)
    n2 = rand_between(block_num[0] - 1, n1 - 1) if n1 > 1 else 1

    color1, color2 = random.sample(colors, 2)

    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    for x, y in all_positions:
        grid_output.fill_cell(x, y, color1)

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n1 + n2
    }

    return grid_input, grid_output, params


def generate_minority_recolor(grid_size=(12, 12), block_num=(2, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n1 = rand_between(*block_num)
    n2 = rand_between(block_num[0] - 1, n1 - 1) if n1 > 1 else 1

    color1, color2 = random.sample(colors, 2)

    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    for x, y in all_positions:
        grid_output.fill_cell(x, y, color2)

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n1 + n2
    }

    return grid_input, grid_output, params



