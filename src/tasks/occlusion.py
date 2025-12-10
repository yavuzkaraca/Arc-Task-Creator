import random
from src.grid import Grid


def generate_occlusion_reversal(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input = Grid(rows, cols)
    grid_output = Grid(rows, cols)

    w, h = random.randint(*size_range), random.randint(*size_range)

    # TODO: update the block location generation logic. Use always top-left corner, calculate valid window from
    #  there. Use rotation to generate other possibilities. This makes non-square and different-size blocks easier.

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
        front_block = {"xmin": x2 - w, "ymin": y2 - h, "xmax": x2, "ymax": y2, "color": colors[1]}

    elif corner == "bl":
        front_block = {"xmin": x2, "ymin": y2, "xmax": x2 + w, "ymax": y2 + h, "color": colors[1]}

    else:
        front_block = {"xmin": x2 - w, "ymin": y2, "xmax": x2, "ymax": y2 + h, "color": colors[1]}

    # Input: back first, front second
    grid_input.fill_rect(**back_block)
    grid_input.fill_rect(**front_block)

    # Output: front first, back second (reversed)
    grid_output.fill_rect(**front_block)
    grid_output.fill_rect(**back_block)

    return grid_input, grid_output


def generate_occlusion_random_transform(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )

    grid_output = grid_input.copy()

    transform = random.choice(("mirror_x", "mirror_y", "rot90", "rot180"))

    if transform == "mirror_x":
        grid_output.mirror_x()
    elif transform == "mirror_y":
        grid_output.mirror_y()
    elif transform == "rot90":
        grid_output.rotate_left_90()
    else:  # "rot180"
        grid_output.rotate_left_90()
        grid_output.rotate_left_90()

    return grid_input, grid_output


def generate_occlusion_mirror_x(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.mirror_x()

    return grid_input, grid_output


def generate_occlusion_mirror_y(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.mirror_y()

    return grid_input, grid_output


def generate_occlusion_rotate_90(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.rotate_left_90()

    return grid_input, grid_output


def generate_occlusion_rotate_180(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.rotate_left_90()
    grid_output.rotate_left_90()

    return grid_input, grid_output
