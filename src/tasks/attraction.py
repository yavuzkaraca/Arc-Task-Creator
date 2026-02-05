import random

from src.grid import Grid
from util import rand_between


def generate_color_attraction(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1, w2, h2 = (rand_between(*size_range) for _ in range(4))

    x1 = rand_between(0, cols - w1 - w2 - 1)
    y1 = rand_between(0, rows - h1 - 1)

    x2 = rand_between(x1 + w1 + 1, cols - w2)
    y2 = rand_between(max(0, y1 - h2 + 1), min(rows - h2, y1 + h1 - 1))

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2 + w2 - 1, ymax=y2 + h2 - 1, color=colors[1])

    grid_output.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_output.fill_rect(xmin=x1 + w1, ymin=y2, xmax=x1 + w1 + w2 - 1, ymax=y2 + h2 - 1, color=colors[1])

    for _ in range(random.randrange(4)):  # 0–3 times
        grid_input.rotate_left_90()
        grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_size_attraction(grid_size=(12, 12), size_range=(3, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1 = (rand_between(*size_range) for _ in range(2))
    w2 = rand_between(1, w1 - 1)
    h2 = rand_between(1, h1 - 1)

    x1 = rand_between(0, cols - w1 - w2 - 1)
    y1 = rand_between(0, rows - h1 - 1)

    x2 = rand_between(x1 + w1 + 1, cols - w2)
    y2 = rand_between(max(0, y1 - h2 + 1), min(rows - h2, y1 + h1 - 1))

    c_big, c_small = random.getrandbits(1), random.getrandbits(1)

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[c_big])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2 + w2 - 1, ymax=y2 + h2 - 1, color=colors[c_small])

    grid_output.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[c_big])
    grid_output.fill_rect(xmin=x1 + w1, ymin=y2, xmax=x1 + w1 + w2 - 1, ymax=y2 + h2 - 1, color=colors[c_small])

    for _ in range(random.randrange(4)):  # 0–3 times
        grid_input.rotate_left_90()
        grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_repulsion_gun(grid_size=(12, 12), size_range=(3, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1 = (rand_between(*size_range) for _ in range(2))
    w2 = rand_between(1, w1)
    h2 = rand_between(1, h1 - 2)

    x1 = rand_between(0, cols - w1 - w2 - 1)
    y1 = rand_between(0, rows - h1 - 1)

    x2 = rand_between(x1 + w1 - w2, x1 + w1 - 1)
    y2 = rand_between(y1 + 1, y1 + h1 - h2 - 1)

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2 + w2 - 1, ymax=y2 + h2 - 1, color=colors[1])

    grid_output.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_output.fill_rect(xmin=cols - w2, ymin=y2, xmax=cols, ymax=y2 + h2 - 1, color=colors[1])

    for _ in range(random.randrange(4)):  # 0–3 times
        grid_input.rotate_left_90()
        grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_repulsion_ambiguous(grid_size=(12, 12), size_range=(1, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1, w2, h2 = (rand_between(*size_range) for _ in range(4))

    x1 = rand_between(0, cols - w1 - w2 - 1)
    y1 = rand_between(0, rows - h1 - 1)

    x2 = rand_between(x1 + 1, x1 + w1 - 1)
    y2 = rand_between(y1 + 1, y1 + h1 - 1)

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2 + w2 - 1, ymax=y2 + h2 - 1, color=colors[1])

    grid_output.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[0])
    grid_output.fill_rect(xmin=cols - w2, ymin=y2, xmax=cols, ymax=y2 + h2 - 1, color=colors[1])

    for _ in range(random.randrange(4)):  # 0–3 times
        grid_input.rotate_left_90()
        grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_gravity(grid_size=(12, 12), size_range=(1, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1, w2, h2 = (rand_between(*size_range) for _ in range(4))

    x1 = rand_between(0, cols - w1 - w2 - 1)
    y1 = rand_between(1, rows - h1 - 1)

    x2 = rand_between(x1 + w1 + 1, cols - w2)
    y2 = rand_between(1, rows - h2 - 1)

    c_big, c_small = random.getrandbits(1), random.getrandbits(1)

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1 + w1 - 1, ymax=y1 + h1 - 1, color=colors[c_big])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2 + w2 - 1, ymax=y2 + h2 - 1, color=colors[c_small])

    grid_output.fill_rect(xmin=x1, ymin=0, xmax=x1 + w1 - 1, ymax=0 + h1 - 1, color=colors[c_big])
    grid_output.fill_rect(xmin=x2, ymin=0, xmax=x2 + w2 - 1, ymax=0 + h2 - 1, color=colors[c_small])

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_float(grid_size=(12, 12), size_range=(1, 6), colors=("red", "blue")):
    grid_input, grid_output, params = generate_gravity(grid_size=grid_size, size_range=size_range, colors=colors)
    # TODO: funny idea
    grid_input.rotate_left_90()
    grid_input.rotate_left_90()
    grid_output.rotate_left_90()
    grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params
