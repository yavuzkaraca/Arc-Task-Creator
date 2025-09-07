from src.tasks.attraction import (generate_color_attraction, generate_size_attraction, generate_repulsion_gun,
                                  generate_repulsion_ambiguous, generate_gravity, generate_float)
from src.tasks.expansion import generate_star_expansion_single_step, generate_star_expansion_full
from src.tasks.occlusion import generate_occlusion_reversal, generate_occlusion_transform
from src.visualize import render_save_grid, render_save_combined_grids
from src.util import next_run_idx


def _save(base, name, idx, input_grid, output_grid):
    prefix = f"{name}.t{idx}"
    render_save_grid(input_grid, f"{base}/{prefix}.input.png")
    render_save_grid(output_grid, f"{base}/{prefix}.output.png")
    render_save_combined_grids(input_grid, output_grid, f"{base}/{prefix}.combined.png")


def main(N):
    tasks = [
        ("occlusion_reversal", generate_occlusion_reversal),
        ("occlusion_transform", generate_occlusion_transform),
        ("attraction_color", generate_color_attraction),
        ("attraction_size", generate_size_attraction),
        ("attraction_gravity", generate_gravity),
        ("attraction_float", generate_float),
        ("repulsion_gun", generate_repulsion_gun),
        ("repulsion_ambiguous", generate_repulsion_ambiguous),
        ("expansion_star_step", generate_star_expansion_single_step),
        ("expansion_star_full", generate_star_expansion_full)
    ]
    for name, gen in tasks:
        for _ in range(N):
            idx, base = next_run_idx(name)
            input_grid, output_grid = gen()
            _save(base, name, idx, input_grid, output_grid)


if __name__ == "__main__":
    main(N=15)
