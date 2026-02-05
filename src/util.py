import os
import random
import re
import json
from typing import Any, Dict, Tuple


def next_run_idx(task_name: str):
    """
    Return (next_index, base_dir) for the given task_name.
    Detects both legacy 'tN/' directories and new 'task.tN.*' files.
    """
    base = os.path.join("out", task_name)
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


def new_seed() -> int:
    """Return a fresh 32-bit seed."""
    return random.randrange(0, 2 ** 32)


def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    """Append one JSON record as a single line (utf-8)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
