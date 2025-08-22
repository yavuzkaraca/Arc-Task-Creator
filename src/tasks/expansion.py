import random

from src.grid import Grid
from src.util import rand_between


def generate_star_expansion_single_step(grid_size=(12, 12), star_num=(1, 4), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = min(rand_between(*star_num), (cols - 2) * (rows - 2))

    centers = random.sample(
        [(x, y) for x in range(1, cols - 1) for y in range(1, rows - 1)],
        n
    )

    for x, y in centers:
        grid_input.fill_cell(x, y, colors[0])

        grid_output.fill_cell(x, y, colors[0])
        grid_output.fill_cell(x + 1, y + 1, colors[1])
        grid_output.fill_cell(x + 1, y - 1, colors[1])
        grid_output.fill_cell(x - 1, y + 1, colors[1])
        grid_output.fill_cell(x - 1, y - 1, colors[1])

    return grid_input, grid_output


def generate_star_expansion_full(grid_size=(12, 12), star_num=(1, 3), colors=("red", "blue")):

    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = min(rand_between(*star_num), max(0, (cols - 2) * (rows - 2)))
    if n == 0:
        return grid_input, grid_output

    centers = random.sample(
        [(x, y) for x in range(1, cols - 1) for y in range(1, rows - 1)],
        n
    )

    # mark centers on input
    for x, y in centers:
        grid_input.fill_cell(x, y, colors[0])

    # directions: four diagonals
    dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    # draw to borders on output
    for x0, y0 in centers:
        grid_output.fill_cell(x0, y0, colors[0])  # center
        for dx, dy in dirs:
            x, y = x0 + dx, y0 + dy
            while 0 <= x < cols and 0 <= y < rows:
                grid_output.fill_cell(x, y, colors[1])
                x += dx
                y += dy

    # TODO: refill the origin points that might have been over-colored

    return grid_input, grid_output
