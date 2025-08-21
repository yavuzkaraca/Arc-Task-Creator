from src.tasks.attraction import (generate_color_attraction, generate_size_attraction, generate_repulsion_gun,
                                  generate_repulsion_ambiguous)
from src.tasks.occlusion import generate_occlusion_reversal
from src.visualize import render_save_grid, render_save_combined_grids
from src.util import next_run_dir


def _save(run_dir, ig, og):
    render_save_grid(ig, f"{run_dir}/input.png")
    render_save_grid(og, f"{run_dir}/output.png")
    render_save_combined_grids(ig, og, f"{run_dir}/combined.png")


def main(N=1):
    tasks = [
        ("occlusion_reversal", generate_occlusion_reversal),
        ("attraction_color", generate_color_attraction),
        ("attraction_size", generate_size_attraction),
        ("repulsion_gun", generate_repulsion_gun),
        ("repulsion_ambiguous", generate_repulsion_ambiguous)
    ]
    for name, gen in tasks:
        for _ in range(N):
            run = next_run_dir(name)
            ig, og = gen()
            _save(run, ig, og)


if __name__ == "__main__":
    main(N=3)
