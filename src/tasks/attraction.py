import random
from src.grid import Grid
from src.visualize import render_grid


def generate_color_attraction(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input = Grid(rows, cols)
    grid_output = Grid(rows, cols)

    w1, h1, w2, h2 = (random.randint(*size_range) for _ in range(4))

    # Always consider attraction to left => moving block on the right. Then we rotate to generate all possibilities.

    x1 = random.randint(0, cols - w1 - w2 - 1)  # -1 bc grid_size index starts at 0
    y1 = random.randint(0, cols - h1 - 1)

    x2 = random.randint(x1 + w1 + 1, cols - w2)
    y2 = random.randint(max(0, y1 - h2 + 1), min(cols - 1, y1 + h1 - 1))

    static_block = {"xmin": x1, "ymin": y1, "xmax": x1 + w1 - 1, "ymax": y1 + h1 - 1, "color": colors[0]}
    moving_block = {"xmin": x2, "ymin": y2, "xmax": x2 + w2 - 1, "ymax": y2 + h2 - 1, "color": colors[1]}

    grid_input.fill_rect(**static_block)
    grid_input.fill_rect(**moving_block)

    render_grid(grid_input)

    grid_output.fill_rect(**static_block)
    moving_block = {"xmin": x1 + w1, "ymin": y2, "xmax": x1 + w1 + w2 - 1, "ymax": y2 + h2 - 1, "color": colors[1]}
    grid_output.fill_rect(**moving_block)

    render_grid(grid_output)

    return grid_input


def generate_size_attraction(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    # TODO: attract according to size i.e. bigger block attracts
    pass
