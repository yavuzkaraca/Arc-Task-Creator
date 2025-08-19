from src.visualize import render_grid, render_grids_together
from src.tasks.occlusion import generate_occlusion_reversal_rectangles
from src.util import get_output_path


def main():
    input_grid, output_grid = generate_occlusion_reversal_rectangles()
    render_grids_together(input_grid, output_grid,
                          save_path=get_output_path("occlusion", "overlap_combined.png"))


if __name__ == '__main__':
    main()
