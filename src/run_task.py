import os
import random

from src.util import next_run_idx, new_seed, append_jsonl
from src.visualize import save_grid, save_combined_grids
from src.stimulus import Stimulus


def run_task(name, gen):

    idx, base = next_run_idx(name.replace(".", "_"))

    seed = new_seed()
    random.seed(seed)

    out = gen()
    inp, out, params = (*out, {})[:3]   # <- python trick

    prefix = f"{name}.t{idx}"

    p_in = os.path.join(base, f"{prefix}.input.png")
    p_out = os.path.join(base, f"{prefix}.output.png")
    p_comb = os.path.join(base, f"{prefix}.combined.png")

    save_grid(inp, p_in)
    save_grid(out, p_out)
    save_combined_grids(inp, out, p_comb)

    stim = Stimulus(
        id=prefix,
        rule=name,
        seed=seed,
        params=params,
        input_grid=inp,
        output_grid=out,
    )

    rec = stim.to_json_dict()
    rec["paths"] = {"input": p_in, "output": p_out, "combined": p_comb}

    append_jsonl(os.path.join(base, "stimuli.jsonl"), rec)
