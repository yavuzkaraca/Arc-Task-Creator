"""
Session builder for ARC-style same/different experiment (fMRI-friendly).

This script creates a `session.json` that a stimulus runner (e.g., Psychtoolbox) can execute.

High-level design
-----------------
A session consists of multiple blocks. Each block contains 4 phases:

  1) phase_start (inference)
     - shows ONE trial (two images) to establish the initial "rule context"

  2) inference
     - decision phase with `n_decisions_per_phase` trials
     - the rule context UPDATES after each trial (swap_context=True)
     - each trial is labeled:
         correct="same"      -> trial uses the current context (family + sub_rule)
         correct="different" -> trial uses a different context (different sub_rule, or different family in mix blocks)

  3) phase_start (application)
     - shows ONE trial (two images) to establish the memorized rule context

  4) application
     - decision phase with `n_decisions_per_phase` trials
     - the rule context stays FIXED (swap_context=False)
     - trials are labeled same/different relative to that fixed context

Block types
-----------
- Family blocks: sampling is restricted to ONE family (restrict_family=<family>).
- Mix blocks: sampling spans ALL families (restrict_family=None).

"Same" vs "Different"
---------------------
Important: "same" means same RULE CONTEXT (same family + sub_rule), not identical images.
Even for "same", two fresh stimuli are sampled (without replacement) from the same pool.

Stimulus input format
---------------------
Expected directory layout:

  out/<rule_dir>/stimuli.jsonl
  out/<rule_dir>/<stim_id>.combined.png

Each JSONL row should contain at least:
  - id:        unique stimulus identifier (used to find <id>.combined.png)
  - rule:      sub_rule string (e.g., "expansion.star_full")
Optional:
  - family:    family string (if missing, inferred as rule.split(".", 1)[0])
  - seed:      generation seed for reproducibility

Output JSON schema (session.json)
--------------------------------
session = {
  "participant": str,
  "keys": {"same": str, "different": str},   # KbName-compatible names (e.g., "LeftArrow")
  "blocks": [block, ...]
}

block = {
  "block_id": int,
  "family": <family name> or "mix",
  "phases": [phase_start, inference, phase_start, application]
}

trial entry = {
  "imgs":   [<relpath-to-first>, <relpath-to-second>],
  "family": str,
  "sub_rule": str,
  "ids":   [id1, id2],
  "seeds": [seed1, seed2],
  "correct": "same" | "different"   # only for decision phases
}

"""

import json
import random
from pathlib import Path


# ---------------- IO ----------------
def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def relpath(path: Path, base_dir: Path) -> str:
    return str(path.resolve().relative_to(base_dir)).replace("\\", "/")


# ---------------- pretty key labels ----------------
DISPLAY_KEY = {
    "LeftArrow": "←",
    "RightArrow": "→",
    "ESCAPE": "Esc",
}


def key_label(key_name: str) -> str:
    return DISPLAY_KEY.get(key_name, key_name)


def tip_pair(left_key: str, left_text: str, right_key: str, right_text: str, gap: int = 10) -> str:
    # Creates: "←   Same          Different   →"
    left = f"{key_label(left_key)}   {left_text}"
    right = f"{right_text}   {key_label(right_key)}"
    return left + (" " * gap) + right


# ---------------- stimuli pool ----------------
def collect_pools(out_root: Path) -> dict[str, dict[str, list[dict]]]:
    """
    Build stimulus pools from `out_root`.

    Returns:
      pools[family][sub_rule] = list of stimulus dicts:
        {"id": <str>, "seed": <int|None>, "combined_path": <Path>}

    Expects:
      out/<rule_dir>/stimuli.jsonl
      out/<rule_dir>/<stim_id>.combined.png

    Notes:
      - sub_rule is read from JSON key "rule"
      - family is read from JSON key "family" or inferred from sub_rule prefix
    """
    pools: dict[str, dict[str, list[dict]]] = {}

    for rule_dir in out_root.iterdir():
        if not rule_dir.is_dir():
            continue

        stim_path = rule_dir / "stimuli.jsonl"
        for stim_meta in load_jsonl(stim_path):
            sub_rule = stim_meta.get("rule")
            stim_id = stim_meta.get("id")
            if not sub_rule or not stim_id:
                continue

            combined_path = rule_dir / f"{stim_id}.combined.png"
            if not combined_path.exists():
                continue

            family = stim_meta.get("family") or sub_rule.split(".", 1)[0] or "unknown"
            pools.setdefault(family, {}).setdefault(sub_rule, []).append(
                {"id": stim_id, "seed": stim_meta.get("seed"), "combined_path": combined_path}
            )

    return pools


# ---------------- picking ----------------
def uid(stimulus: dict) -> str:
    return str(stimulus.get("id") or stimulus["combined_path"])


def available_pairs(pool: list[dict], used_stimuli_ids: set[str]) -> int:
    return sum(1 for stimulus in pool if uid(stimulus) not in used_stimuli_ids) // 2


def pick_pair(pool: list[dict], rng: random.Random, used_stimuli_ids: set[str]) -> tuple[dict, dict]:
    unused = [stimulus for stimulus in pool if uid(stimulus) not in used_stimuli_ids]
    if len(unused) < 2:
        raise ValueError("Not enough unused stimuli for a pair.")
    rng.shuffle(unused)
    stim_first, stim_second = unused[0], unused[1]
    used_stimuli_ids.add(uid(stim_first))
    used_stimuli_ids.add(uid(stim_second))
    return stim_first, stim_second


def pick_sub_rule(
        family_pool: dict[str, list[dict]],
        rng: random.Random,
        used_stimuli_ids: set[str],
        avoid: str | None = None
) -> str:
    candidate_sub_rules = [
        sub_rule
        for sub_rule, pool in family_pool.items()
        if sub_rule != avoid and available_pairs(pool, used_stimuli_ids) >= 1
    ]
    if not candidate_sub_rules:
        raise ValueError("No sub_rule has enough remaining pairs.")
    return rng.choice(candidate_sub_rules)


def pick_any(
        pools: dict[str, dict[str, list[dict]]],
        rng: random.Random,
        used_stimuli_ids: set[str],
        avoid: tuple[str, str] | None = None,
        restrict_family: str | None = None
) -> tuple[str, str]:
    candidate_contexts: list[tuple[str, str]] = []
    family_items = [(restrict_family, pools[restrict_family])] if restrict_family else pools.items()

    for family, family_pool in family_items:
        for sub_rule, pool in family_pool.items():
            if avoid and (family, sub_rule) == avoid:
                continue
            if available_pairs(pool, used_stimuli_ids) >= 1:
                candidate_contexts.append((family, sub_rule))

    if not candidate_contexts:
        raise ValueError("No (family, sub_rule) has enough remaining pairs.")
    return rng.choice(candidate_contexts)


def trial_entry(
        family: str,
        sub_rule: str,
        pair: tuple[dict, dict],
        base_dir: Path,
        correct: str | None = None
) -> dict:
    stim_first, stim_second = pair
    trial = {
        "imgs": [relpath(stim_first["combined_path"], base_dir), relpath(stim_second["combined_path"], base_dir)],
        "family": family,
        "sub_rule": sub_rule,
        "ids": [stim_first.get("id"), stim_second.get("id")],
        "seeds": [stim_first.get("seed"), stim_second.get("seed")],
    }
    if correct in ("same", "different"):
        trial["correct"] = correct
    return trial


# ---------------- phase building ----------------
def make_phase_start(
        family: str,
        sub_rule: str,
        pools,
        rng,
        used_stimuli_ids,
        base_dir,
        bg: str,
        hint: str,
        tip: str
) -> dict:
    pair = pick_pair(pools[family][sub_rule], rng, used_stimuli_ids)
    return {
        "phase": "phase_start",
        "bg": bg,
        "hint": hint,
        "tip": tip,
        "trial": [trial_entry(family, sub_rule, pair, base_dir)],
    }


def make_decision_phase(
        name: str,
        pools,
        rng: random.Random,
        used_stimuli_ids: set[str],
        base_dir: Path,
        n_trials: int,
        p_same: float,
        bg: str,
        hint: str,
        tip: str,
        context: tuple[str, str],
        swap_context: bool,
        restrict_family: str | None = None,
) -> tuple[dict, tuple[str, str]]:
    """
    Create a decision phase (inference or application).

    Parameters:
      context = (context_family, context_sub_rule)
      swap_context:
        - True  -> context becomes the context sampled for each trial (inference)
        - False -> context stays the same across trials (application)

      restrict_family:
        - None       -> sample across all families (mix block)
        - <family>   -> sample only within that family (family block)

    Trial labeling:
      - correct="same": sampled (family, sub_rule) equals current context
      - correct="different": sampled context differs from current context
    """
    context_family, context_sub_rule = context
    trials: list[dict] = []

    for _ in range(n_trials):
        want_same = rng.random() < p_same

        # Decide which context to sample for this trial
        if want_same:
            sub_rule_pool = pools.get(context_family, {}).get(context_sub_rule, [])
            if (restrict_family is None or context_family == restrict_family) and available_pairs(sub_rule_pool, used_stimuli_ids) >= 1:
                family, sub_rule, correct = context_family, context_sub_rule, "same"
            else:
                family, sub_rule = pick_any(
                    pools, rng, used_stimuli_ids,
                    avoid=(context_family, context_sub_rule),
                    restrict_family=restrict_family,
                )
                correct = "different"
        else:
            family, sub_rule = pick_any(
                pools, rng, used_stimuli_ids,
                avoid=(context_family, context_sub_rule),
                restrict_family=restrict_family,
            )
            correct = "different"

        pair = pick_pair(pools[family][sub_rule], rng, used_stimuli_ids)
        trials.append(trial_entry(family, sub_rule, pair, base_dir, correct=correct))

        if swap_context:
            context_family, context_sub_rule = family, sub_rule

    phase = {"phase": name, "bg": bg, "hint": hint, "tip": tip, "trials": trials}
    return phase, (context_family, context_sub_rule)


# ---------------- session builder ----------------
def build_session(
        out_root: str = "out",
        participant: str = "p001",
        session_path: str = "session.json",
        seed: int = 2,  # Change seed to get different session TODO: convert participant id for the seed
        key_same: str = "LeftArrow",
        key_diff: str = "RightArrow",
        n_family_blocks: int = 6,
        n_mix_blocks: int = 2,
        n_decisions_per_phase: int = 8,
        p_same_inference: float = 0.5,
        p_same_application: float = 0.5,
        inference_bg: str = "green",
        inference_hint: str = "Previous rule",
        application_bg: str = "red",
        application_hint: str = "Memorized rule",
):
    rng = random.Random(seed)
    out_base = Path(out_root).resolve()
    session_file = Path(session_path).resolve()
    base_dir = session_file.parent.resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    pools = collect_pools(out_base)
    families = sorted(pools.keys())
    rng.shuffle(families)

    TIP_READY = tip_pair(key_same, "Ready", key_diff, "Ready")
    TIP_MEMO = tip_pair(key_same, "Memorized", key_diff, "Memorized")
    TIP_DECIDE = tip_pair(key_same, "Same", key_diff, "Different")

    def build_block(block_id: int, restrict_family: str | None) -> dict:
        used_stimuli_ids: set[str] = set()

        # ---- phase_start + inference (context updates each trial) ----
        first_family, first_sub_rule = pick_any(pools, rng, used_stimuli_ids, restrict_family=restrict_family)
        phase_start_inference = make_phase_start(
            first_family, first_sub_rule, pools, rng, used_stimuli_ids, base_dir,
            inference_bg, "First rule", TIP_READY
        )

        inference_phase, (context_family, context_sub_rule) = make_decision_phase(
            "inference", pools, rng, used_stimuli_ids, base_dir,
            n_decisions_per_phase, p_same_inference,
            inference_bg, inference_hint, TIP_DECIDE,
            context=(first_family, first_sub_rule),
            swap_context=True,
            restrict_family=restrict_family,
        )

        # ---- phase_start + application (context fixed across trials) ----
        memorized_family, memorized_sub_rule = pick_any(pools, rng, used_stimuli_ids, restrict_family=restrict_family)
        phase_start_application = make_phase_start(
            memorized_family, memorized_sub_rule, pools, rng, used_stimuli_ids, base_dir,
            application_bg, "Memorize this rule", TIP_MEMO
        )

        application_phase, _ = make_decision_phase(
            "application", pools, rng, used_stimuli_ids, base_dir,
            n_decisions_per_phase, p_same_application,
            application_bg, application_hint, TIP_DECIDE,
            context=(memorized_family, memorized_sub_rule),
            swap_context=False,
            restrict_family=restrict_family,
        )

        family_label = restrict_family if restrict_family else "mix"
        return {
            "block_id": block_id,
            "family": family_label,
            "phases": [phase_start_inference, inference_phase, phase_start_application, application_phase],
        }

    blocks: list[dict] = []
    next_block_id = 1

    # ---- family-restricted blocks ----
    for family in families[:n_family_blocks]:
        try:
            blocks.append(build_block(next_block_id, restrict_family=family))
            next_block_id += 1
        except ValueError:
            pass

    # ---- mixed blocks ----
    for _ in range(n_mix_blocks):
        try:
            blocks.append(build_block(next_block_id, restrict_family=None))
            next_block_id += 1
        except ValueError:
            break

    session = {
        "participant": participant,
        "keys": {"same": key_same, "different": key_diff},
        "blocks": blocks,
    }
    session_file.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Wrote:", session_file)
    print("Blocks:", len(blocks), f"(target: {n_family_blocks + n_mix_blocks})")
    for block in blocks:
        n_items = sum(len(phase.get("trial", [])) + len(phase.get("trials", [])) for phase in block["phases"])
        print(f"  block {block['block_id']:02d} family={block['family']} items={n_items}")


if __name__ == "__main__":
    build_session()
