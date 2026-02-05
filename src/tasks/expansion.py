import random

from src.grid import Grid
from util import rand_between


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

        grid_output.fill_cell(x + 1, y + 1, colors[1])
        grid_output.fill_cell(x + 1, y - 1, colors[1])
        grid_output.fill_cell(x - 1, y + 1, colors[1])
        grid_output.fill_cell(x - 1, y - 1, colors[1])

    for x, y in centers:
        grid_output.fill_cell(x, y, colors[0])  # refill the origin points that might have been over-colored

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params


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

    for x, y in centers:
        grid_input.fill_cell(x, y, colors[0])

    dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    for x0, y0 in centers:
        for dx, dy in dirs:
            x, y = x0 + dx, y0 + dy
            while 0 <= x < cols and 0 <= y < rows:
                grid_output.fill_cell(x, y, colors[1])
                x += dx
                y += dy

    for x0, y0 in centers:
        grid_output.fill_cell(x0, y0, colors[0])  # refill the origin points that might have been over-colored

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params


def generate_plus_expansion_single_step(grid_size=(12, 12), plus_num=(1, 4), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = min(rand_between(*plus_num), (cols - 2) * (rows - 2))
    centers = random.sample(
        [(x, y) for x in range(1, cols - 1) for y in range(1, rows - 1)],
        n
    )

    for x, y in centers:
        grid_input.fill_cell(x, y, colors[0])

        grid_output.fill_cell(x + 1, y, colors[1])
        grid_output.fill_cell(x - 1, y, colors[1])
        grid_output.fill_cell(x, y + 1, colors[1])
        grid_output.fill_cell(x, y - 1, colors[1])

    for x, y in centers:
        grid_output.fill_cell(x, y, colors[0])  # refill the origin points that might have been over-colored

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params


def generate_plus_expansion_full(grid_size=(12, 12), plus_num=(1, 3), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = min(rand_between(*plus_num), max(0, (cols - 2) * (rows - 2)))
    if n == 0:
        return grid_input, grid_output

    centers = random.sample(
        [(x, y) for x in range(1, cols - 1) for y in range(1, rows - 1)],
        n
    )

    for x, y in centers:
        grid_input.fill_cell(x, y, colors[0])

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for x0, y0 in centers:
        for dx, dy in dirs:
            x, y = x0 + dx, y0 + dy
            while 0 <= x < cols and 0 <= y < rows:
                grid_output.fill_cell(x, y, colors[1])
                x += dx
                y += dy

    for x0, y0 in centers:
        grid_output.fill_cell(x0, y0, colors[0])  # refill the origin points that might have been over-colored

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params


def generate_3diagonal_expansion_full(grid_size=(12, 12), star_num=(1, 3), colors=("red", "blue")):
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

    # four diagonal directions
    dirs_all = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    for x0, y0 in centers:
        # randomly choose one diagonal to *omit*
        dirs = list(dirs_all)
        skip_dir = random.choice(dirs)
        dirs.remove(skip_dir)

        for dx, dy in dirs:
            x, y = x0 + dx, y0 + dy
            while 0 <= x < cols and 0 <= y < rows:
                grid_output.fill_cell(x, y, colors[1])
                x += dx
                y += dy

    for x0, y0 in centers:
        grid_output.fill_cell(x0, y0, colors[0])  # refill the origin points that might have been over-colored

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params
