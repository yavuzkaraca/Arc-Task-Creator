import os


def next_run_dir(task_name: str) -> str:
    base = os.path.join("../out", task_name)
    os.makedirs(base, exist_ok=True)
    idx = 1 + max([int(d[1:]) for d in os.listdir(base) if d.startswith("t") and d[1:].isdigit()] or [0])
    run = os.path.join(base, f"t{idx}")
    os.makedirs(run, exist_ok=True)
    return run
