import json
import random
from pathlib import Path


# ---------------- IO ----------------
def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def relpath(p: Path, base: Path) -> str:
    return str(p.resolve().relative_to(base)).replace("\\", "/")


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
    family -> sub_rule -> [{id, seed, combined_path}]
    Expects: out/<sub_rule>/stimuli.jsonl and <id>.combined.png in same folder.
    """
    pools: dict[str, dict[str, list[dict]]] = {}

    for rule_dir in out_root.iterdir():
        if not rule_dir.is_dir():
            continue

        stim_path = rule_dir / "stimuli.jsonl"
        for row in load_jsonl(stim_path):
            sub_rule = row.get("rule")
            stim_id = row.get("id")
            if not sub_rule or not stim_id:
                continue

            comb = rule_dir / f"{stim_id}.combined.png"
            if not comb.exists():
                continue

            fam = row.get("family") or sub_rule.split(".", 1)[0] or "unknown"
            pools.setdefault(fam, {}).setdefault(sub_rule, []).append(
                {"id": stim_id, "seed": row.get("seed"), "combined_path": comb}
            )

    return pools


# ---------------- picking ----------------
def uid(stim: dict) -> str:
    return str(stim.get("id") or stim["combined_path"])


def available_pairs(pool: list[dict], used: set[str]) -> int:
    return sum(1 for stim in pool if uid(stim) not in used) // 2


def pick_pair(pool: list[dict], rng: random.Random, used: set[str]) -> tuple[dict, dict]:
    unused = [stim for stim in pool if uid(stim) not in used]
    if len(unused) < 2:
        raise ValueError("Not enough unused stimuli for a pair.")
    rng.shuffle(unused)
    stim_first, stim_second = unused[0], unused[1]
    used.add(uid(stim_first))
    used.add(uid(stim_second))
    return stim_first, stim_second


def pick_subrule(fam_pool: dict[str, list[dict]], rng: random.Random, used: set[str], avoid: str | None = None) -> str:
    cands = [subrule for subrule, pool in fam_pool.items() if subrule != avoid and available_pairs(pool, used) >= 1]
    if not cands:
        raise ValueError("No sub_rule has enough remaining pairs.")
    return rng.choice(cands)


def pick_any(pools: dict[str, dict[str, list[dict]]],
             rng: random.Random,
             used: set[str],
             avoid: tuple[str, str] | None = None,
             restrict_family: str | None = None) -> tuple[str, str]:
    cands: list[tuple[str, str]] = []
    fam_items = [(restrict_family, pools[restrict_family])] if restrict_family else pools.items()

    for fam, fam_pool in fam_items:
        for subrule, pool in fam_pool.items():
            if avoid and (fam, subrule) == avoid:
                continue
            if available_pairs(pool, used) >= 1:
                cands.append((fam, subrule))

    if not cands:
        raise ValueError("No (family, sub_rule) has enough remaining pairs.")
    return rng.choice(cands)


def trial_entry(family: str, sub_rule: str, pair: tuple[dict, dict], base_dir: Path,
                correct: str | None = None) -> dict:
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
def make_phase_start(fam: str, sr: str, pools, rng, used, base_dir, bg: str, hint: str, tip: str) -> dict:
    pair = pick_pair(pools[fam][sr], rng, used)
    return {"phase": "phase_start", "bg": bg, "hint": hint, "tip": tip,
            "trial": [trial_entry(fam, sr, pair, base_dir)]}


def make_decision_phase(
        name: str,
        pools,
        rng: random.Random,
        used: set[str],
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
    context_family, context_subrule = context
    trials: list[dict] = []

    for _ in range(n_trials):
        want_same = rng.random() < p_same

        if want_same:
            # try same as context, otherwise force different
            subrule_pool = pools.get(context_family, {}).get(context_subrule, [])
            if (restrict_family is None or context_family == restrict_family) and available_pairs(subrule_pool,
                                                                                                  used) >= 1:
                family, subrule, correct = context_family, context_subrule, "same"
            else:
                family, subrule = pick_any(
                    pools, rng, used,
                    avoid=(context_family, context_subrule),
                    restrict_family=restrict_family
                )
                correct = "different"
        else:
            family, subrule = pick_any(
                pools, rng, used,
                avoid=(context_family, context_subrule),
                restrict_family=restrict_family
            )
            correct = "different"

        pair = pick_pair(pools[family][subrule], rng, used)
        trials.append(trial_entry(family, subrule, pair, base_dir, correct=correct))

        if swap_context:
            context_family, context_subrule = family, subrule

    return {"phase": name, "bg": bg, "hint": hint, "tip": tip, "trials": trials}, (context_family, context_subrule)


# ---------------- session builder ----------------
def build_session(
        out_root: str = "out",
        participant: str = "p001",
        session_path: str = "session.json",
        seed: int = 42,
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
        used_stimuli: set[str] = set()

        # pick first context
        first_family, first_subrule = pick_any(pools, rng, used_stimuli, restrict_family=restrict_family)
        phase_start_inference = make_phase_start(
            first_family, first_subrule, pools, rng, used_stimuli, base_dir,
            inference_bg, "First rule", TIP_READY
        )

        inference_phase, (context_family, context_subrule) = make_decision_phase(
            "inference", pools, rng, used_stimuli, base_dir,
            n_decisions_per_phase, p_same_inference,
            inference_bg, inference_hint, TIP_DECIDE,
            context=(first_family, first_subrule),
            swap_context=True,
            restrict_family=restrict_family,
        )

        # pick memorized rule context
        memorized_family, memorized_subrule = pick_any(pools, rng, used_stimuli, restrict_family=restrict_family)
        phase_start_application = make_phase_start(
            memorized_family, memorized_subrule, pools, rng, used_stimuli, base_dir,
            application_bg, "Memorize this rule", TIP_MEMO
        )

        application_phase, _ = make_decision_phase(
            "application", pools, rng, used_stimuli, base_dir,
            n_decisions_per_phase, p_same_application,
            application_bg, application_hint, TIP_DECIDE,
            context=(memorized_family, memorized_subrule),
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

    # family-restricted blocks
    for family in families[:n_family_blocks]:
        try:
            blocks.append(build_block(next_block_id, restrict_family=family))
            next_block_id += 1
        except ValueError:
            pass

    # mixed blocks
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
