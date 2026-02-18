import json
import random
from pathlib import Path


# ---------------- IO ----------------
def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def relpath(p: Path, base: Path) -> str:
    return str(p.resolve().relative_to(base)).replace("\\", "/")


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

        for rec in load_jsonl(rule_dir / "stimuli.jsonl"):
            sub_rule = rec.get("rule")
            stim_id = rec.get("id")
            if not sub_rule or not stim_id:
                continue

            comb = rule_dir / f"{stim_id}.combined.png"
            if not comb.exists():
                continue

            fam = rec.get("family") or sub_rule.split(".", 1)[0] or "unknown"
            pools.setdefault(fam, {}).setdefault(sub_rule, []).append(
                {"id": stim_id, "seed": rec.get("seed"), "combined_path": comb}
            )

    return pools


# ---------------- picking ----------------
def uid(stim: dict) -> str:
    return str(stim.get("id") or stim["combined_path"])


def available_pairs(pool: list[dict], used: set[str]) -> int:
    return sum(1 for s in pool if uid(s) not in used) // 2


def pick_pair(pool: list[dict], rng: random.Random, used: set[str]) -> tuple[dict, dict]:
    unused = [s for s in pool if uid(s) not in used]
    if len(unused) < 2:
        raise ValueError("Not enough unused stimuli for a pair.")
    rng.shuffle(unused)
    a, b = unused[0], unused[1]
    used.add(uid(a))
    used.add(uid(b))
    return a, b


def pick_subrule(fam_pool: dict[str, list[dict]], rng: random.Random, used: set[str], avoid: str | None = None) -> str:
    cands = [sr for sr, pool in fam_pool.items()
             if sr != avoid and available_pairs(pool, used) >= 1]
    if not cands:
        raise ValueError("No sub_rule has enough remaining pairs.")
    return rng.choice(cands)


def pick_subrule_diff(fam_pool: dict[str, list[dict]], rng: random.Random, used: set[str], avoid: str) -> str:
    return pick_subrule(fam_pool, rng, used, avoid=avoid)


def pick_any(pools: dict[str, dict[str, list[dict]]],
             rng: random.Random,
             used: set[str],
             avoid: tuple[str, str] | None = None) -> tuple[str, str]:
    cands: list[tuple[str, str]] = []
    for fam, fam_pool in pools.items():
        for sr, pool in fam_pool.items():
            if avoid and (fam, sr) == avoid:
                continue
            if available_pairs(pool, used) >= 1:
                cands.append((fam, sr))
    if not cands:
        raise ValueError("No (family, sub_rule) has enough remaining pairs.")
    return rng.choice(cands)


def trial_entry(family: str, sub_rule: str, pair: tuple[dict, dict], base_dir: Path,
                correct: str | None = None) -> dict:
    a, b = pair
    d = {
        "imgs": [relpath(a["combined_path"], base_dir), relpath(b["combined_path"], base_dir)],
        "family": family,
        "sub_rule": sub_rule,
        "ids": [a.get("id"), b.get("id")],
        "seeds": [a.get("seed"), b.get("seed")],
    }
    if correct in ("same", "different"):
        d["correct"] = correct
    return d


# ---------------- phases ----------------
def phase_start(family: str, sub_rule: str, pools: dict[str, dict[str, list[dict]]],
                rng: random.Random, used: set[str], base_dir: Path, bg: str, hint: str, tip: str) -> dict:
    pair = pick_pair(pools[family][sub_rule], rng, used)
    return {"phase": "phase_start", "bg": bg, "hint": hint, "tip": tip,
            "trial": [trial_entry(family, sub_rule, pair, base_dir)]}


def decision_phase(
        name: str,
        pools: dict[str, dict[str, list[dict]]],
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
        restrict_family: str | None = None,  # NEW
) -> tuple[dict, tuple[str, str]]:
    ctx_fam, ctx_sr = context
    trials: list[dict] = []

    for _ in range(n_trials):
        want_same = rng.random() < p_same

        # ---------- pick next (fam, subrule) ----------
        if restrict_family is None:
            # MIX: unrestricted
            if want_same:
                pool = pools.get(ctx_fam, {}).get(ctx_sr, [])
                if available_pairs(pool, used) >= 1:
                    fam, sr, correct = ctx_fam, ctx_sr, "same"
                else:
                    fam, sr = pick_any(pools, rng, used, avoid=(ctx_fam, ctx_sr))
                    correct = "different"
            else:
                fam, sr = pick_any(pools, rng, used, avoid=(ctx_fam, ctx_sr))
                correct = "different"

        else:
            # FAMILY BLOCK: restricted to one family
            fam = restrict_family
            fam_pool = pools[fam]

            if want_same:
                pool = fam_pool.get(ctx_sr, [])
                if ctx_fam == fam and available_pairs(pool, used) >= 1:
                    sr, correct = ctx_sr, "same"
                else:
                    sr = pick_subrule(fam_pool, rng, used, avoid=ctx_sr)
                    correct = "different"
            else:
                sr = pick_subrule(fam_pool, rng, used, avoid=ctx_sr)
                correct = "different"

        pair = pick_pair(pools[fam][sr], rng, used)
        trials.append(trial_entry(fam, sr, pair, base_dir, correct=correct))

        if swap_context:
            ctx_fam, ctx_sr = fam, sr

    phase = {"phase": name, "bg": bg, "hint": hint, "tip": tip, "trials": trials}
    return phase, (ctx_fam, ctx_sr)


# ---------------- session builder ----------------
def build_session(
        out_root: str = "out",
        participant: str = "p001",
        session_path: str = "session.json",
        seed: int = 42,
        keys_same: str = "LeftArrow",
        keys_diff: str = "RightArrow",
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

    def build_family_block(block_id: int, fam: str) -> dict:
        used: set[str] = set()
        fam_pool = pools[fam]

        # ---- Inference: phase_start establishes the first context sub_rule (within family) ----
        sr0 = pick_subrule(fam_pool, rng, used)
        ps_inf = phase_start(
            fam, sr0, pools, rng, used, base_dir,
            inference_bg, "First rule",
            "←   Ready          Ready   →"
        )

        inf, ctx = decision_phase(
            "inference", pools, rng, used, base_dir,
            n_decisions_per_phase, p_same_inference,
            inference_bg, inference_hint,
            "←   Same          Different   →",
            context=(fam, sr0),
            swap_context=True,
            restrict_family=fam,  # <-- IMPORTANT
        )

        # ---- Application: phase_start establishes the memorized sub_rule (within family) ----
        srM = pick_subrule(fam_pool, rng, used)
        ps_app = phase_start(
            fam, srM, pools, rng, used, base_dir,
            application_bg, "Memorize this rule",
            "←   Memorized          Memorized   →"
        )

        app, _ = decision_phase(
            "application", pools, rng, used, base_dir,
            n_decisions_per_phase, p_same_application,
            application_bg, application_hint,
            "←   Same          Different   →",
            context=(fam, srM),
            swap_context=False,
            restrict_family=fam,  # <-- IMPORTANT
        )

        return {"block_id": block_id, "family": fam, "phases": [ps_inf, inf, ps_app, app]}

    def build_mix_block(block_id: int) -> dict:
        used: set[str] = set()

        fam0, sr0 = pick_any(pools, rng, used)
        ps_inf = phase_start(fam0, sr0, pools, rng, used, base_dir,
                             inference_bg, "First rule", f"{keys_same} = Got it    {keys_diff} = Got it")

        inf, ctx = decision_phase("inference", pools, rng, used, base_dir,
                                  n_decisions_per_phase, p_same_inference,
                                  inference_bg, inference_hint, f"{keys_same} = SAME    {keys_diff} = DIFFERENT",
                                  context=(fam0, sr0), swap_context=True)

        famM, srM = pick_any(pools, rng, used)
        ps_app = phase_start(famM, srM, pools, rng, used, base_dir,
                             application_bg, "Memorize this rule",
                             f"{keys_same} = Memorized    {keys_diff} = Memorized")

        app, _ = decision_phase("application", pools, rng, used, base_dir,
                                n_decisions_per_phase, p_same_application,
                                application_bg, application_hint, f"{keys_same} = SAME    {keys_diff} = DIFFERENT",
                                context=(famM, srM), swap_context=False)

        return {"block_id": block_id, "family": "mix", "phases": [ps_inf, inf, ps_app, app]}

    blocks: list[dict] = []
    block_id = 1

    for fam in families[:n_family_blocks]:
        try:
            blocks.append(build_family_block(block_id, fam))
            block_id += 1
        except ValueError:
            pass

    for _ in range(n_mix_blocks):
        try:
            blocks.append(build_mix_block(block_id))
            block_id += 1
        except ValueError:
            break

    session = {"participant": participant, "keys": {"same": keys_same, "different": keys_diff}, "blocks": blocks}
    session_file.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Wrote:", session_file)
    print("Blocks:", len(blocks), f"(target: {n_family_blocks + n_mix_blocks})")
    for b in blocks:
        n_items = sum(len(p.get("trial", [])) + len(p.get("trials", [])) for p in b["phases"])
        print(f"  block {b['block_id']:02d} family={b['family']} items={n_items}")


if __name__ == "__main__":
    build_session()
