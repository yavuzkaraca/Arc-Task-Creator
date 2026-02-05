import random
from pathlib import Path

from src.visualize import save_grid, save_combined_grids
from src.stimulus import Stimulus
from util import append_jsonl, next_idx, new_seed

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


def main(N=3):
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
            _generate_task(name, gen)


def _generate_task(rule: str, gen, out_root: str = "out") -> None:
    base = Path(out_root) / rule
    base.mkdir(parents=True, exist_ok=True)
    jsonl_path = base / "stimuli.jsonl"

    idx = next_idx(jsonl_path)
    seed = new_seed()
    random.seed(seed)

    produced = gen()
    inp, out, params = (*produced, {})[:3]

    stim_id = f"{rule}.t{idx}"
    p_in = base / f"{stim_id}.input.png"
    p_out = base / f"{stim_id}.output.png"
    p_comb = base / f"{stim_id}.combined.png"

    save_grid(inp, str(p_in))
    save_grid(out, str(p_out))
    save_combined_grids(inp, out, str(p_comb))

    family = rule.split(".", 1)[0]

    stim = Stimulus(
        id=stim_id,
        rule=rule,
        family=family,
        seed=seed,
        params=params,
        input_grid=inp,
        output_grid=out,
    )

    rec = stim.to_json_dict()
    rec["paths"] = {"input": str(p_in), "output": str(p_out), "combined": str(p_comb)}

    append_jsonl(jsonl_path, rec)


if __name__ == "__main__":
    main()
