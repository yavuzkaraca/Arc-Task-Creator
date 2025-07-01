import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def render_grid(grid, save_path="output.png"):
    rows, cols = grid.rows, grid.cols
    color_grid = grid.as_list()

    # Convert color names/hex to normalized RGB
    rgb_grid = np.array([
        [mcolors.to_rgb(color_grid[r][c]) for c in range(cols)]
        for r in range(rows)
    ])

    fig, ax = plt.subplots(figsize=(cols, rows))
    fig.patch.set_facecolor("gray")
    ax.imshow(rgb_grid, interpolation='none', extent=(0, cols, rows, 0))

    # Draw vertical and horizontal gridlines
    for x in range(cols + 1):
        ax.axvline(x, color='gray', linewidth=2)
    for y in range(rows + 1):
        ax.axhline(y, color='gray', linewidth=2)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig(save_path, dpi=100, bbox_inches='tight', pad_inches=0.03)

    plt.close()
