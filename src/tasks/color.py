import random

from util import rand_between
from src.grid import Grid


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

    return grid_input, grid_output


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

    return grid_input, grid_output


PLUS_OFFSETS = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]          # 2,4,5,6,8
CROSS_OFFSETS = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]         # 1,3,5,7,9


def _stamp_cells(top_r: int, top_c: int, offsets):
    """Return absolute (row, col) cells for a 3x3 stamp at top-left (top_r, top_c)."""
    return [(top_r + dr, top_c + dc) for dr, dc in offsets]


def generate_cross_plus_recolor(
    grid_size=(12, 12),
    stamp_num=(2, 6),
    bg_color="black",
    input_shape_color="gray",
    cross_color="red",
    plus_color="blue",
):
    """
    Place several 3x3 stamps (either CROSS or PLUS) on the grid without overlap.
    Input: all stamp cells are gray.
    Output: stamp cells recolored by shape (cross->red, plus->blue).
    """
    rows, cols = grid_size
    grid_input, grid_output = Grid(rows, cols, default_color=bg_color), Grid(rows, cols, default_color=bg_color)

    k = rand_between(*stamp_num)

    # Candidate top-left positions where a 3x3 fits
    candidates = [(r, c) for r in range(rows - 2) for c in range(cols - 2)]
    random.shuffle(candidates)

    used_cells = set()
    placed = []

    for top_r, top_c in candidates:
        shape = random.choice(["cross", "plus"])
        offsets = CROSS_OFFSETS if shape == "cross" else PLUS_OFFSETS
        cells = _stamp_cells(top_r, top_c, offsets)

        # Ensure all cells are inside and non-overlapping (stamps may touch, but not share cells)
        if any((r, c) in used_cells for r, c in cells):
            continue

        placed.append((shape, cells))
        for r, c in cells:
            used_cells.add((r, c))

        if len(placed) >= k:
            break

    # Fill input
    for _, cells in placed:
        for r, c in cells:
            grid_input.fill_cell(r, c, input_shape_color)

    # Fill output: recolor by shape
    for shape, cells in placed:
        out_color = cross_color if shape == "cross" else plus_color
        for r, c in cells:
            grid_output.fill_cell(r, c, out_color)

    return grid_input, grid_output
