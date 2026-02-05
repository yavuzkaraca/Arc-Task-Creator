from src.tasks.color import (
    generate_cross_plus_recolor,
    generate_inversion_recolor,
    generate_odd_color_recolor,
)

from src.tasks.arithmetic import (
    generate_majority_recolor,
    generate_minority_recolor,

)
from src.tasks.expansion import (
    generate_star_expansion_single_step,
    generate_star_expansion_full,
    generate_plus_expansion_single_step,
    generate_plus_expansion_full,
    generate_3diagonal_expansion_full,
)
from src.tasks.occlusion import (
    generate_occlusion_reversal,
    generate_occlusion_mirror_x,
    generate_occlusion_mirror_y,
    generate_occlusion_rotate_90,
    generate_occlusion_rotate_180,
)
from src.tasks.attraction import (
    generate_color_attraction,
    generate_size_attraction,
    generate_repulsion_gun,
    generate_repulsion_ambiguous,
    generate_gravity,
    generate_float,
)

from src.run_task import run_task


# Comment out or in tasks here to limit generation

def main(N=15):
    tasks = {
        # ("occlusion_reversal": generate_occlusion_reversal),
        # ("occlusion_mirror_x": generate_occlusion_mirror_x),
        # ("occlusion_mirror_y": generate_occlusion_mirror_y),
        # ("occlusion_rotate_90": generate_occlusion_rotate_90),
        # ("occlusion_rotate_180": generate_occlusion_rotate_180),
        # ("attraction_color": generate_color_attraction),
        # ("attraction_size": generate_size_attraction),
        # ("attraction_gravity": generate_gravity),
        # ("attraction_float": generate_float),
        # ("attraction_repulsion_gun": generate_repulsion_gun),
        # ("attraction_repulsion_ambiguous": generate_repulsion_ambiguous),
        # ("expansion_star_step": generate_star_expansion_single_step),
        # ("expansion_star_full": generate_star_expansion_full),
        # ("expansion_plus_step": generate_plus_expansion_single_step),
        # ("expansion_plus_full": generate_plus_expansion_full),
        # ("expansion_3diagonal_full": generate_3diagonal_expansion_full),
        # ("arithmetic_majority_recolor": generate_majority_recolor),
        # ("arithmetic_minority_recolor": generate_minority_recolor),
        # ("arithmetic_parity_recolor": generate_parity_recolor),
        # ("color_inversion_recolor": generate_inversion_recolor),
        # ("color_odd_recolor": generate_odd_color_recolor),
        "color.cross_plus_recolor": generate_cross_plus_recolor,
    }

    for name, gen in tasks.items():
        for _ in range(N):
            run_task(name, gen)


if __name__ == "__main__":
    main()
