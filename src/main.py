from src.tasks.attraction import (generate_color_attraction, generate_size_attraction, generate_repulsion_gun,
                                  generate_repulsion_ambiguous, generate_gravity, generate_float)
from src.tasks.expansion import (generate_star_expansion_single_step, generate_star_expansion_full,
                                 generate_plus_expansion_full, generate_plus_expansion_single_step,
                                 generate_3diagonal_expansion_full)
from src.tasks.occlusion import (generate_occlusion_reversal, generate_occlusion_transform_random,
                                 generate_occlusion_rotate_180, generate_occlusion_rotate_90,
                                 generate_occlusion_mirror_x, generate_occlusion_mirror_y)
from src.tasks.arithmetic import (generate_majority_recolor, generate_minority_recolor, generate_parity_recolor,
                                  generate_inversion_recolor)

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
        ("occlusion_mirror_x", generate_occlusion_mirror_x),
        ("occlusion_mirror_y", generate_occlusion_mirror_y),
        ("occlusion_rotate_90", generate_occlusion_rotate_90),
        ("occlusion_rotate_180", generate_occlusion_rotate_180),
        ("attraction_color", generate_color_attraction),
        ("attraction_size", generate_size_attraction),
        ("attraction_gravity", generate_gravity),
        ("attraction_float", generate_float),
        ("attraction_repulsion_gun", generate_repulsion_gun),
        ("attraction_repulsion_ambiguous", generate_repulsion_ambiguous),
        ("expansion_star_step", generate_star_expansion_single_step),
        ("expansion_star_full", generate_star_expansion_full),
        ("expansion_plus_step", generate_plus_expansion_single_step),
        ("expansion_plus_full", generate_plus_expansion_full),
        ("expansion_3diagonal_full", generate_3diagonal_expansion_full),
        ("arithmetic_majority_recolor", generate_majority_recolor),
        ("arithmetic_minority_recolor", generate_minority_recolor),
        ("arithmetic_parity_recolor", generate_parity_recolor),
        ("arithmetic_inversion_recolor", generate_inversion_recolor)
    ]

    for name, gen in tasks:
        for _ in range(N):
            idx, base = next_run_idx(name)
            input_grid, output_grid = gen()
            _save(base, name, idx, input_grid, output_grid)


if __name__ == "__main__":
    main(N=15)
