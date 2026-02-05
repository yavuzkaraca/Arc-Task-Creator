import json
import random
from pathlib import Path

from src.visualize import save_grid, save_combined_grids
from src.stimulus import Stimulus


def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _next_idx(jsonl_path: Path) -> int:
    if not jsonl_path.exists():
        return 1
    with jsonl_path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f) + 1


def _new_seed() -> int:
    # 32-bit seed; stable across platforms
    return random.randrange(0, 2**32)


def generate_task(rule: str, gen, out_root: str = "out") -> None:
    base = Path(out_root) / rule
    base.mkdir(parents=True, exist_ok=True)
    jsonl_path = base / "stimuli.jsonl"

    idx = _next_idx(jsonl_path)
    seed = _new_seed()
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
        provenance={"generator": "ArcTaskCreator"},
    )

    rec = stim.to_json_dict()
    rec["paths"] = {"input": str(p_in), "output": str(p_out), "combined": str(p_comb)}

    _append_jsonl(jsonl_path, rec)
