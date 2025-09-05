import os
import random
from typing import Tuple


def next_run_dir(task_name: str) -> str:
    """
    Outdated due to web app not working with folders
    """
    base = os.path.join("../out", task_name)
    os.makedirs(base, exist_ok=True)
    idx = 1 + max([int(d[1:]) for d in os.listdir(base) if d.startswith("t") and d[1:].isdigit()] or [0])
    run = os.path.join(base, f"t{idx}")
    os.makedirs(run, exist_ok=True)
    return run


def next_run_idx(task_name: str) -> tuple[int, str]:
    base = os.path.join("../out", task_name)
    os.makedirs(base, exist_ok=True)
    idx = 1 + max(
        [int(f[1:].split(".")[0]) for f in os.listdir(base) if f.startswith("t") and f[1:2].isdigit()]
        or [0]
    )
    return idx, base


def rand_between(a, b):
    return random.randint(a, b) if a < b else a
