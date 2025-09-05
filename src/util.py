import os
import random
import re


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


def next_run_idx(task_name: str):
    """
    Return (next_index, base_dir) for the given task_name.
    Detects both legacy 'tN/' directories and new 'task.tN.*' files.
    """
    base = os.path.join("../out", task_name)
    os.makedirs(base, exist_ok=True)

    max_idx = 0
    for entry in os.listdir(base):
        m_legacy = re.fullmatch(r"t(\d+)", entry)
        if m_legacy:
            max_idx = max(max_idx, int(m_legacy.group(1)))
            continue

        m_flat = re.match(rf"{re.escape(task_name)}\.t(\d+)\.", entry)
        if m_flat:
            max_idx = max(max_idx, int(m_flat.group(1)))

    return max_idx + 1, base


def rand_between(a, b):
    return random.randint(a, b) if a < b else a
