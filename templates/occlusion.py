import random
from grid import Grid


def generate_occlusion_reversal_samesize(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input = Grid(rows, cols)
    grid_output = Grid(rows, cols)

    # Random sizes for both blocks
    w, h = random.randint(*size_range), random.randint(*size_range)

    # Random position for back block (x and y of bottom left corner of the back block)
    x1 = random.randint(min(size_range), cols - w - min(size_range))
    y1 = random.randint(min(size_range), rows - h - min(size_range))
    back_block = {"xmin": x1, "ymin": y1, "xmax": x1 + w, "ymax": y1 + h, "color": colors[0]}

    # (x and y can be any corner of the front block)
    min_x2 = x1 + 1
    max_x2 = x1 + w - 1
    min_y2 = y1 + 1
    max_y2 = y1 + h - 1

    x2 = random.randint(min_x2, max_x2)
    y2 = random.randint(min_y2, max_y2)

    # Pick a corner of front block
    corner = random.choice(["tl", "tr", "bl", "br"])

    if corner == "tl":
        front_block = {"xmin": x2, "ymin": y2 - h, "xmax": x2 + w, "ymax": y2, "color": colors[1]}

    elif corner == "tr":
        front_block = {"xmin": x2-w, "ymin": y2 - h, "xmax": x2, "ymax": y2, "color": colors[1]}

    elif corner == "bl":
        front_block = {"xmin": x2, "ymin": y2, "xmax": x2 + w, "ymax": y2 + h, "color": colors[1]}

    else:
        front_block = {"xmin": x2-w, "ymin": y2, "xmax": x2, "ymax": y2 + h, "color": colors[1]}

    # Input: back first, front second
    grid_input.fill_rect(**back_block)
    grid_input.fill_rect(**front_block)

    # Output: front first, back second (reversed)
    grid_output.fill_rect(**front_block)
    grid_output.fill_rect(**back_block)

    return grid_input, grid_output


def generate_occlusion_reversal_difsize(grid_size=(12, 12), size_range=(3, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input = Grid(rows, cols)
    grid_output = Grid(rows, cols)

    # Random sizes for both blocks
    w1, h1 = random.randint(*size_range), random.randint(*size_range)

    # Random position for back block (x and y of bottom left corner)
    x1 = random.randint(0, cols - w1)
    y1 = random.randint(0, rows - h1)

    # Pick a corner of front block
    corner = random.choice(["tl", "tr", "bl", "br"])

    # Calculate front block corner based on chosen corner alignment
    if corner == "tl":
        min_x = x1 + 1 + (w1 - w2)
        max_x = x1 + w1 - 1
        min_y = y1 + 1
        max_y = min(y1 + h1 - h2, rows - h2)
    elif corner == "tr":
        min_x = max(x1 + w2 - 1, x1 + 1)
        max_x = x1 + w1 - 2
        min_y = y1 + 1
        max_y = min(y1 + h1 - h2, rows - h2)

    elif corner == "bl":
        min_x = x1 + 1
        max_x = min(x1 + w1 - w2, cols - w2)
        min_y = max(y1 + h2 - 1, y1 + 1)
        max_y = y1 + h1 - 2

    elif corner == "br":
        min_x = max(x1 + w2 - 1, x1 + 1)
        max_x = x1 + w1 - 2
        min_y = max(y1 + h2 - 1, y1 + 1)
        max_y = y1 + h1 - 2

    x2 = min_x if min_x == max_x else random.randint(min_x, max_x)
    y2 = min_y if min_y == max_y else random.randint(min_y, max_y)

    # Clamp within grid
    x2 = max(0, min(x2, cols - w2))
    y2 = max(0, min(y2, rows - h2))

    # Place back block first
    back_block = {"xmin": x1, "ymin": y1, "xmax": x1 + w1, "ymax": y1 + h1, "color": colors[0]}
    front_block = {"xmin": x2, "ymin": y2, "xmax": x2 + w2, "ymax": y2 + h2, "color": colors[1]}

    # Input: back first, front second
    grid_input.fill_rect(**back_block)
    grid_input.fill_rect(**front_block)

    # Output: front first, back second (reversed)
    grid_output.fill_rect(**front_block)
    grid_output.fill_rect(**back_block)

    return grid_input, grid_output
