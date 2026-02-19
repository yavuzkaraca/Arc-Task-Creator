import random
from typing import Dict, Tuple, Any, List
from src.grid import Grid
from src.util import rand_between


def generate_inversion_recolor(grid_size=(12, 12), block_num=(1, 6), colors=("red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n1 = rand_between(*block_num)
    n2 = rand_between(*block_num)

    color1, color2 = random.sample(colors, 2)

    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n1 + n2)
    color1_positions = all_positions[:n1]
    color2_positions = all_positions[n1:]

    for x, y in color1_positions:
        grid_input.fill_cell(x, y, color1)
    for x, y in color2_positions:
        grid_input.fill_cell(x, y, color2)

    for x, y in color1_positions:
        grid_output.fill_cell(x, y, color2)
    for x, y in color2_positions:
        grid_output.fill_cell(x, y, color1)

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n1+n2
    }

    return grid_input, grid_output, params


def generate_odd_color_recolor(grid_size=(12, 12), block_num=(3, 12), colors=("red", "blue")):
    """
    Input: all blocks are one color except one block (odd color).
    Output: all blocks become the odd color.
    """
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    n = rand_between(*block_num)
    n = max(n, 2)  # need at least 2 blocks to have "one odd, rest majority"

    majority_color, odd_color = random.sample(colors, 2)

    all_positions = random.sample([(x, y) for x in range(cols) for y in range(rows)], n)
    odd_pos = random.choice(all_positions)

    # Fill input
    for x, y in all_positions:
        grid_input.fill_cell(x, y, majority_color)
    grid_input.fill_cell(*odd_pos, odd_color)

    # Fill output: all positions become odd color
    for x, y in all_positions:
        grid_output.fill_cell(x, y, odd_color)

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": n
    }

    return grid_input, grid_output, params


# Needed for cross plus recolor
OFFSETS = {
    "plus": [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # 2,4,5,6,8
    "cross": [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],  # 1,3,5,7,9
}


def generate_cross_plus_recolor(grid_size=(12, 12), stamp_num=(2, 6), colors=("gray", "red", "blue")):
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols), Grid(rows, cols)

    k = rand_between(*stamp_num)
    out_map = {"cross": colors[1], "plus": colors[2]}

    candidates = [(r, c) for r in range(rows - 2) for c in range(cols - 2)]
    random.shuffle(candidates)

    used = set()
    placed: List[Tuple[str, List[Tuple[int, int]]]] = []

    for top_r, top_c in candidates:
        shape = random.choice(("cross", "plus"))
        cells = [(top_r + dr, top_c + dc) for dr, dc in OFFSETS[shape]]
        if any(cell in used for cell in cells):
            continue
        used.update(cells)
        placed.append((shape, cells))
        if len(placed) == k:
            break

    for shape, cells in placed:
        for r, c in cells:
            grid_input.fill_cell(r, c, colors[0])
            grid_output.fill_cell(r, c, out_map[shape])

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": len(placed)
    }

    return grid_input, grid_output, params
