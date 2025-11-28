import pandas as pd

UNWANTED_COLS = [
    "code", "confirmationCode", "consent", "correctResponse",
    "example_1", "example_2", "meta", "openLabId", "project",
    "status", "type", "time_commit", "time_end", "time_render",
    "time_run", "time_show", "time_switch", "task",
    "applies", "response_action", "sender_type"
]

PARTICIPANT_COLS = [
    "age", "educational_level", "occupation", "gender",
    "fb_attention", "fb_confidence", "fb_difficulty",
    "fb_strategy_text", "fb_strategy_used"
]

CLEANED_COLS = UNWANTED_COLS + PARTICIPANT_COLS

DESIRED_ORDER = [
    "anon_id", "sender", "sender_id", "block_type",
    "task_id", "super_rule", "sub_rule",
    "response", "correct",
    "difficulty", "duration", "timestamp"
]

CONF_MAP = {
    "Very Sure": 1.0,
    "Sure": 0.70,
    "Unsure": 0.30,
    "Very Unsure": 0.0
}


# ----------------- Cleaning -----------------

def load_csv(path):
    return pd.read_csv(path)


def clean_columns(df):
    return df.drop(columns=CLEANED_COLS, errors="ignore")


def remove_empty_rows(df):
    return df.dropna(how="all")


def keep_only_rows_with_response(df):
    return df[df["ended_on"].astype(str).str.contains("response", na=False)]


def remove_column_ended_on(df):
    return df.drop(columns=["ended_on"], errors="ignore")


def fix_correct_for_rule_reminders(df):
    df.loc[df["sender"] == "Rule Reminder", "correct"] = ""
    return df


def assign_block_type(df):
    def f(t):
        s = str(t).lower()
        if s.startswith("p"): return "practice"
        try:
            return "inference" if int(s) % 10 <= 4 else "application"
        except:
            return ""

    df["block_type"] = df["task_id"].apply(f)
    return df


def assign_anonymous_participant_ids(df):
    ids, pid, cur, prev = [], 1, "t1", False
    for s in df["sender_id"].fillna("").astype(str):
        if prev and s == "4_0_0":
            pid += 1;
            cur = f"t{pid}"
        ids.append(cur)
        prev = (s == "6_3_4")
    df["anon_id"] = ids
    return df


def adjust_confidence_responses(df):
    mapping = {"d": "Very Unsure", "f": "Unsure", "j": "Sure", "k": "Very Sure"}
    m = df["sender"] == "Confidence Check"
    df.loc[m, "response"] = df.loc[m, "response"].astype(str).str.strip().map(mapping).fillna(df.loc[m, "response"])
    return df


def adjust_decision_responses(df):
    mapping = {"y": "Same", "n": "Different"}
    m = df["sender"].isin(["Inference Decision", "Application Decision"])
    df.loc[m, "response"] = df.loc[m, "response"].astype(str).str.strip().map(mapping).fillna(df.loc[m, "response"])
    return df


def clean_difficulty(df):
    df["difficulty"] = (
        df["difficulty"].astype(str).str.replace(".0", "", regex=False).replace("nan", None)
    )
    df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce").astype("Int64")
    return df


def reorder_columns(df):
    ordered = [c for c in DESIRED_ORDER if c in df.columns]
    rest = [c for c in df.columns if c not in ordered]
    return df[ordered + rest]


def assign_anon_id_raw(df: pd.DataFrame) -> pd.DataFrame:
    ids = []
    pid = 0

    for s in df["sender_id"].fillna("").astype(str):
        if s == "0":  # new participant begins
            pid += 1
        ids.append(f"t{pid}")

    df["anon_id"] = ids
    return df


# ----------------- Pipeline -----------------

def preprocess(path):
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


def extract_participant_demographics_from_raw(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)

    raw = assign_anon_id_raw(raw)

    demo_rows = raw[raw[PARTICIPANT_COLS].notna().any(axis=1)]

    demo = (
        demo_rows.groupby("anon_id")
        .agg(lambda x: x.dropna().iloc[0] if x.notna().any() else None)
        .reset_index()
    )

    return demo[["anon_id"] + PARTICIPANT_COLS]


# ----------------- Stats -----------------

def keep_only_real_trials(df):
    df["task_int"] = pd.to_numeric(df["task_id"], errors="coerce")
    r = df[df["task_int"].between(0, 39)]
    return r.drop(columns=["task_int"])


def compute_participant_stats(df):
    s = df.groupby("anon_id").agg(
        total_correct=("correct", lambda x: (x == True).sum()),
        mean_duration=("duration", "mean")
    )
    s["total_trials"] = 40
    s["accuracy"] = s["total_correct"] / 40
    return s.reset_index()


def compute_difficulty_stats(df):
    s = df.groupby("difficulty").agg(
        total_correct=("correct", lambda x: (x == True).sum()),
        total_trials=("correct", lambda x: x.notna().sum()),
        mean_duration=("duration", "mean")
    )
    s["accuracy"] = s["total_correct"] / s["total_trials"]
    return s.reset_index()


def compute_task_stats(df):
    df = df.copy()
    df["conf_num"] = df["response"].map(CONF_MAP).astype(float)

    s = (
        df.groupby("task_id")
        .agg(
            total_correct=("correct", lambda x: (x == True).sum()),
            total_trials=("correct", lambda x: x.isin([True, False]).sum()),
            avg_confidence=("conf_num", "mean"),
            difficulty=("difficulty", lambda x: x.dropna().iloc[0]),
            super_rule=("super_rule", lambda x: x.dropna().iloc[0]),
            sub_rule=("sub_rule", lambda x: x.dropna().iloc[0]),
            mean_duration=("duration", "mean")
        )
        .reset_index()
    )
    s["accuracy"] = s["total_correct"] / s["total_trials"]
    return s


def compute_rule_stats(df):
    r = df.dropna(subset=["super_rule", "sub_rule"], how="all")
    sup = (
        r.dropna(subset=["super_rule"])
        .groupby("super_rule")
        .agg(total_correct=("correct", lambda x: (x == True).sum()),
             total_trials=("correct", lambda x: x.notna().sum()),
             mean_duration=("duration", "mean"))
        .reset_index()
    )
    sup["sub_rule"] = ""

    sub = (
        r.dropna(subset=["sub_rule"])
        .groupby(["super_rule", "sub_rule"])
        .agg(total_correct=("correct", lambda x: (x == True).sum()),
             total_trials=("correct", lambda x: x.notna().sum()),
             mean_duration=("duration", "mean"))
        .reset_index()
    )

    s = pd.concat([sup, sub], ignore_index=True)
    s["accuracy"] = s["total_correct"] / s["total_trials"]
    return s.sort_values(["super_rule", "sub_rule"]).reset_index(drop=True)


def compute_global_stats(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df["correct"].isin([True, False])]

    stats = {
        "mean_accuracy": (valid["correct"] == True).mean(),
        "std_accuracy": (valid["correct"] == True).std(),

        "mean_duration": valid["duration"].mean(),
        "std_duration": valid["duration"].std(),

        "n_participants": df["anon_id"].nunique(),
        "n_trials": len(valid)
    }

    return pd.DataFrame([stats]).round(3)


def compute_duration_stats(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[df["correct"].isin([True, False])]

    stats = {
        "mean_duration": valid["duration"].mean(),
        "median_duration": valid["duration"].median(),
        "iqr_25": valid["duration"].quantile(0.25),
        "iqr_75": valid["duration"].quantile(0.75),
        "n_trials": len(valid),
    }

    return pd.DataFrame([stats]).round(2)
