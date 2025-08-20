from src.tasks.attraction import generate_color_attraction
from src.visualize import render_save_grid, render_grids_together
from src.tasks.occlusion import generate_occlusion_reversal_rectangles
from src.util import get_output_path


def main():
    input_grid, output_grid = generate_occlusion_reversal_rectangles()
    render_save_grid(input_grid, save_path=get_output_path("occlusion", "input.png"))
    render_save_grid(output_grid, save_path=get_output_path("occlusion", "output.png"))
    render_grids_together(input_grid, output_grid,
                          save_path=get_output_path("occlusion", "input_output_combined.png"))

    input_grid, output_grid = generate_color_attraction()
    render_save_grid(input_grid, save_path=get_output_path("attraction", "input.png"))
    render_save_grid(output_grid, save_path=get_output_path("attraction", "output.png"))
    render_grids_together(input_grid, output_grid,
                          save_path=get_output_path("attraction", "input_output_combined.png"))


if __name__ == '__main__':
    main()
