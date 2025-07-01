from grid import Grid
from grid_renderer import render_grid
from templates.occlusion import generate_occlusion_reversal_samesize
from util import get_output_path


def main():
    grid = Grid(10, 10)
    grid.fill_cell(0, 0, "#00ffff")
    grid.fill_rect(xmin=2, xmax=4, ymin=2, ymax=3, color="lime")
    grid.fill_rect(xmin=6, xmax=8, ymin=6, ymax=8, color="#ff00ff")
    render_grid(grid, save_path="test_grid.png")

    input_grid, output_grid = generate_occlusion_reversal_samesize()

    render_grid(input_grid, save_path=get_output_path("occlusion", "overlap_input.png"))
    render_grid(output_grid, save_path=get_output_path("occlusion", "overlap_output.png"))



if __name__ == '__main__':
    main()
