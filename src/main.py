from src.tasks.attraction import generate_color_attraction
from src.tasks.occlusion import generate_occlusion_reversal_rectangles
from src.visualize import render_save_grid, render_save_combined_grids
from src.util import next_run_dir


def _save(run_dir, ig, og):
    render_save_grid(ig, f"{run_dir}/input.png")
    render_save_grid(og, f"{run_dir}/output.png")
    render_save_combined_grids(ig, og, f"{run_dir}/input_output_combined.png")


def main(N=1):
    tasks = [
        ("occlusion", generate_occlusion_reversal_rectangles),
        ("attraction", generate_color_attraction),
    ]
    for name, gen in tasks:
        for _ in range(N):
            run = next_run_dir(name)  # t1, t2, ...
            ig, og = gen()
            _save(run, ig, og)


if __name__ == "__main__":
    main(N=3)
