import random
from src.grid import Grid


def generate_color_attraction(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    w1, h1, w2, h2 = (random.randint(*size_range) for _ in range(4))

    x1 = random.randint(0, cols - w1 - w2 - 1)
    y1 = random.randint(0, rows - h1 - 1)

    x2 = random.randint(x1 + w1 + 1, cols - w2)
    y2 = random.randint(max(0, y1 - h2 + 1), min(rows - h2, y1 + h1 - 1))

    grid_input.fill_rect(xmin=x1, ymin=y1, xmax=x1+w1-1, ymax=y1+h1-1, color=colors[0])
    grid_input.fill_rect(xmin=x2, ymin=y2, xmax=x2+w2-1, ymax=y2+h2-1, color=colors[1])

    grid_output.fill_rect(xmin=x1, ymin=y1, xmax=x1+w1-1, ymax=y1+h1-1, color=colors[0])
    grid_output.fill_rect(xmin=x1+w1, ymin=y2, xmax=x1+w1+w2-1, ymax=y2+h2-1, color=colors[1])

    return grid_input, grid_output


def generate_size_attraction(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    # TODO: attract according to size i.e. bigger block attracts
    pass
