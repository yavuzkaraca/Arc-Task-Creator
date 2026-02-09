import json
import random
from pathlib import Path


# ---------- helpers ----------
def load_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    out = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def relpath(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


def pick_examples_and_trials(items: list[dict], n_examples: int, n_trials: int, rng: random.Random):
    # items must have "combined_path" keys
    rng.shuffle(items)
    ex = items[:n_examples]
    tr = items[n_examples:n_examples + n_trials]
    return ex, tr


# ---------- main ----------
def build_manifest(
        out_root: str = "out",
        participant: str = "p001",
        manifest_path: str = "manifest.json",
        seed: int = 123,
        keys_same: str = "LeftArrow",
        keys_diff: str = "RightArrow",
        use_fmri: bool = False,
        trigger_key: str = "5%",
        disdaq: int = 4,
        phase_name: str = "train",
        bg: str = "green",
        tip: str = "Same = left, Different = right",
        n_examples_per_block: int = 2,
        n_trials_per_block: int = 20,
):
    rng = random.Random(seed)
    out_base = Path(out_root).resolve()
    manifest_file = Path(manifest_path).resolve()
    base_dir = manifest_file.parent.resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    # Collect all stimulus records by family
    # Your generator writes out/<rule>/stimuli.jsonl and PNGs in the same folder.
    by_family: dict[str, list[dict]] = {}

    for rule_dir in out_base.iterdir():
        if not rule_dir.is_dir():
            continue

        jsonl = rule_dir / "stimuli.jsonl"
        recs = load_jsonl(jsonl)

        # If there is no jsonl, still try to find *.combined.png
        if not recs:
            for comb in sorted(rule_dir.glob("*.combined.png")):
                # family inferred from directory name before dot if possible
                # rule_dir.name is e.g. "color.cross_plus_recolor" or "attraction.gravity_dots"
                family = rule_dir.name.split(".", 1)[0]
                by_family.setdefault(family, []).append({
                    "family": family,
                    "combined_path": comb,
                })
            continue

        for rec in recs:
            stim_id = rec["id"]  # e.g. "color.cross_plus_recolor.t1"
            family = rec.get("family") or rec.get("rule", "").split(".", 1)[0] or "unknown"
            comb = rule_dir / f"{stim_id}.combined.png"
            if not comb.exists():
                # fallback: skip if missing
                continue
            by_family.setdefault(family, []).append({
                "family": family,
                "rule": rec.get("rule"),
                "id": stim_id,
                "seed": rec.get("seed"),
                "combined_path": comb,
            })

    # Build blocks
    blocks = []
    block_id = 1
    for family in sorted(by_family.keys()):
        items = by_family[family]
        if len(items) < (n_examples_per_block + 1):
            # Not enough to form examples + at least one trial
            continue

        examples, trials = pick_examples_and_trials(items, n_examples_per_block, n_trials_per_block, rng)

        phase = {
            "phase": phase_name,
            "bg": bg,
            "tip": tip,
            "example_images": [relpath(e["combined_path"], base_dir) for e in examples],
            "trials": [{"img": relpath(t["combined_path"], base_dir)} for t in trials],
        }

        blocks.append({
            "block_id": block_id,
            "family": family,
            "phases": [phase],
        })
        block_id += 1

    manifest = {
        "participant": participant,
        "keys": {"same": keys_same, "different": keys_diff},
        "fmri": {"use": use_fmri, "trigger_key": trigger_key, "disdaq": disdaq},
        "blocks": blocks,
    }

    with manifest_file.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Wrote: {manifest_file}")
    print(f"Blocks: {len(blocks)}")
    for b in blocks:
        ntr = sum(len(ph["trials"]) for ph in b["phases"])
        print(f"  block {b['block_id']:02d} family={b['family']} trials={ntr}")


if __name__ == "__main__":
    # Example usage
    build_manifest(
        out_root="out",
        participant="p001",
        manifest_path="manifest.json",
        seed=42,
        n_examples_per_block=2,
        n_trials_per_block=30,
        use_fmri=False,
        bg="green",
        phase_name="train",
    )
