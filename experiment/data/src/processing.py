import pandas as pd
import matplotlib.pyplot as plt

# ====== Config ======

UNWANTED_COLS = [
    "code", "confirmationCode", "consent", "correctResponse",
    "example_1", "example_2", "meta", "openLabId", "project",
    "status", "type", "time_commit", "time_end", "time_render",
    "time_run", "time_show", "time_switch", "task",
    "applies", "response_action", "sender_type"
]

LATER_NEEDED_COLS = [
    "age", "educational_level", "occupation", "gender",
    "fb_attention", "fb_confidence", "fb_difficulty",
    "fb_strategy_text", "fb_strategy_used"
]

CLEANED_COLS = UNWANTED_COLS + LATER_NEEDED_COLS

DESIRED_ORDER = [
    "anon_id", "sender", "sender_id", "block_type",
    "task_id", "super_rule", "sub_rule",
    "response", "correct",
    "difficulty", "duration", "timestamp"
]

CONF_MAP = {
    "Very Sure": 0.70,
    "Sure": 0.30,
    "Unsure": 0.0,
    "Very Unsure": 0.0
}

colors = {
    1: "#75aacb",  # light blue
    2: "#4b748c",  # medium blue
    3: "#244152",  # dark blue
}
separator_color = "#002d43"  # dark purple


# ====== Basic Cleaning ======

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows.")
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=CLEANED_COLS, errors="ignore")


def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all")


def keep_only_rows_with_response(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["ended_on"].astype(str).str.contains("response", na=False)
    return df[mask]


def remove_column_ended_on(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["ended_on"], errors="ignore")


# ====== Trial Transformations ======

def fix_correct_for_rule_reminders(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["sender"] == "Rule Reminder"
    df.loc[mask, "correct"] = ""
    return df


def assign_block_type(df: pd.DataFrame) -> pd.DataFrame:
    def classify(t):
        s = str(t).strip().lower()
        if s.startswith("p"):
            return "practice"
        try:
            return "inference" if int(s) % 10 <= 4 else "application"
        except:
            return ""

    df["block_type"] = df["task_id"].apply(classify)
    return df


def assign_anonymous_participant_ids(df: pd.DataFrame) -> pd.DataFrame:
    anon_ids = []
    pid = 1
    current = f"t{pid}"
    prev_end = False

    for sender in df["sender_id"].fillna("").astype(str).str.strip():
        if prev_end and sender == "4_0_0":
            pid += 1
            current = f"t{pid}"
        anon_ids.append(current)
        prev_end = sender == "6_3_4"

    df["anon_id"] = anon_ids
    return df


def adjust_confidence_responses(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {"d": "Very Unsure", "f": "Unsure", "j": "Sure", "k": "Very Sure"}
    mask = df["sender"] == "Confidence Check"
    df.loc[mask, "response"] = df.loc[mask, "response"].astype(str).str.strip().map(mapping).fillna(
        df.loc[mask, "response"])
    return df


def adjust_decision_responses(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {"y": "Same", "n": "Different"}
    mask = df["sender"].isin(["Inference Decision", "Application Decision"])
    df.loc[mask, "response"] = df.loc[mask, "response"].astype(str).str.strip().map(mapping).fillna(
        df.loc[mask, "response"])
    return df


def clean_difficulty(df: pd.DataFrame) -> pd.DataFrame:
    df["difficulty"] = (
        df["difficulty"].astype(str).str.replace(".0", "", regex=False)
        .replace("nan", None)
    )
    df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce").astype("Int64")
    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    ordered = [c for c in DESIRED_ORDER if c in df.columns]
    rest = [c for c in df.columns if c not in ordered]
    return df[ordered + rest]


# ====== Analysis ======

def keep_only_real_trials(df: pd.DataFrame) -> pd.DataFrame:
    def to_int(x):
        try:
            return int(str(x))
        except:
            return None

    df["task_id_int"] = df["task_id"].apply(to_int)
    real = df[df["task_id_int"].between(0, 39)]
    return real.drop(columns=["task_id_int"])


def compute_participant_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby("anon_id").agg(
        total_correct=("correct", lambda x: (x == True).sum()),
        mean_duration=("duration", "mean")
    )
    stats["total_trials"] = 40
    stats["accuracy"] = stats["total_correct"] / 40
    return stats.reset_index()


def compute_difficulty_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby("difficulty").agg(
        total_correct=("correct", lambda x: (x == True).sum()),
        total_trials=("correct", lambda x: x.notna().sum()),
        mean_duration=("duration", "mean")
    )
    stats["accuracy"] = stats["total_correct"] / stats["total_trials"]
    return stats.reset_index()


def compute_task_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Per-task accuracy, confidence, difficulty, super/sub-rule."""

    df = df.copy()
    df["conf_num"] = df["response"].map(CONF_MAP).astype(float)

    stats = (
        df.groupby("task_id")
        .agg(
            total_correct=("correct", lambda x: (x == True).sum()),
            total_trials=("correct", lambda x: x.isin([True, False]).sum()),
            avg_confidence=("conf_num", "mean"),
            difficulty=("difficulty", lambda x: x.dropna().iloc[0]),
            super_rule=("super_rule", lambda x: x.dropna().iloc[0]),
            sub_rule=("sub_rule", lambda x: x.dropna().iloc[0]),
            mean_duration=("duration", "mean"),
        )
        .reset_index()
    )

    stats["accuracy"] = stats["total_correct"] / stats["total_trials"]
    return stats


def compute_rule_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Stats per super_rule and per sub_rule (sub_rule blank for super)."""
    r = df.dropna(subset=["super_rule", "sub_rule"], how="all")

    # --- Super rules ---
    super_stats = (
        r.dropna(subset=["super_rule"])
        .groupby("super_rule")
        .agg(total_correct=("correct", lambda x: (x == True).sum()),
             total_trials=("correct", lambda x: x.notna().sum()),
             mean_duration=("duration", "mean"))
        .reset_index()
    )
    super_stats["sub_rule"] = ""

    # --- Sub rules ---
    sub_stats = (
        r.dropna(subset=["sub_rule"])
        .groupby(["super_rule", "sub_rule"])
        .agg(total_correct=("correct", lambda x: (x == True).sum()),
             total_trials=("correct", lambda x: x.notna().sum()),
             mean_duration=("duration", "mean"))
        .reset_index()
    )

    # --- Combine ---
    stats = pd.concat([super_stats, sub_stats], ignore_index=True)
    stats["accuracy"] = stats["total_correct"] / stats["total_trials"]

    # Sort: first by super rule, then sub rule
    return stats.sort_values(
        by=["super_rule", "sub_rule"]
    ).reset_index(drop=True)


# ====== Pipeline ======

def preprocess(path: str) -> pd.DataFrame:
    df = load_csv(path)
    df = clean_columns(df)
    df = remove_empty_rows(df)
    df = keep_only_rows_with_response(df)
    df = remove_column_ended_on(df)
    df = fix_correct_for_rule_reminders(df)
    df = assign_block_type(df)
    df = assign_anonymous_participant_ids(df)
    df = adjust_confidence_responses(df)
    df = adjust_decision_responses(df)
    df = clean_difficulty(df)
    return reorder_columns(df)


# ====== Plots ======

import matplotlib.pyplot as plt

def plot_task_accuracy_hierarchical(task_stats):
    ts = task_stats.copy()
    ts["task_id"] = ts["task_id"].astype(int)
    ts = ts.sort_values("task_id")

    colors = {
        1: "#e6e1ff",  # light blue
        2: "#aaa6c4",  # medium blue
        3: "#646982",  # dark blue
    }
    bar_colors = ts["difficulty"].map(colors)

    fig, ax = plt.subplots(figsize=(14, 6))

    # --- Bar plot ---
    ax.bar(ts["task_id"], ts["accuracy"], color=bar_colors, edgecolor="black")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Accuracy")
    ax.set_xticks(ts["task_id"])
    ax.set_xticklabels(ts["task_id"])

    # separators (nice purple)
    for x in [9.5, 19.5, 29.5]:
        ax.axvline(x, color="#252440", linewidth=5, linestyle="--")

    # --- INNER (5-wide) BLOCK SPANS ---
    for i in range(0, 40, 5):
        label = "Inf" if (i % 10) < 5 else "App"
        x0, x1 = i - 0.4, i + 4 + 0.4
        y = -0.08
        ax.plot([x0, x1], [y, y], transform=ax.get_xaxis_transform(), color="black")
        ax.text((x0 + x1) / 2, y - 0.02, label,
                ha="center", va="top", transform=ax.get_xaxis_transform())

    # --- OUTER (10-wide) FAMILY SPANS ---
    families = ["Expansion", "Attraction", "Occlusion", "Arithmetic"]
    for i, fam in zip(range(0, 40, 10), families):
        x0, x1 = i - 0.4, i + 9 + 0.4
        y = -0.20
        ax.plot([x0, x1], [y, y], transform=ax.get_xaxis_transform(),
                color="black", linewidth=1.2)
        ax.text((x0 + x1) / 2, y - 0.02, fam,
                ha="center", va="top", transform=ax.get_xaxis_transform())

    # --- LEGEND ---
    from matplotlib.patches import Patch

    legend_handles = [
        Patch(facecolor="#e6e1ff", edgecolor="black", label="Difficulty 1"),
        Patch(facecolor="#aaa6c4", edgecolor="black", label="Difficulty 2"),
        Patch(facecolor="#646982", edgecolor="black", label="Difficulty 3"),
    ]

    ax.legend(
        handles=legend_handles,
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="black"
    )

    plt.subplots_adjust(bottom=0.25)
    plt.title("Task Accuracy")
    plt.grid(axis="y", alpha=0.3)
    plt.show()



# ====== Main ======

if __name__ == "__main__":
    df = preprocess("../data.csv")
    df.to_csv("processed_data.csv", index=False)

    real = keep_only_real_trials(df)

    participant_stats = compute_participant_stats(real)
    difficulty_stats = compute_difficulty_stats(real)
    rule_stats = compute_rule_stats(real)
    task_stats = compute_task_stats(real)

    task_stats.to_csv("task_stats.csv", index=False)
    participant_stats.to_csv("participant_stats.csv", index=False)
    difficulty_stats.to_csv("difficulty_stats.csv", index=False)
    rule_stats.to_csv("rule_stats.csv", index=False)

    plot_task_accuracy_hierarchical(task_stats)

    print("All done.")
