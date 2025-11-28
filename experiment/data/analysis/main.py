from pathlib import Path

from processing import (
    preprocess, keep_only_real_trials,
    compute_participant_stats, compute_difficulty_stats,
    compute_rule_stats, compute_task_stats, compute_global_stats, compute_duration_stats
)
from plots import plot_task_accuracy_hierarchical, plot_task_accuracy_hierarchical_plain, plot_rule_stats, \
    plot_participant_accuracy, plot_participant_scatter


def main():
    ROOT = Path(__file__).resolve().parent.parent  # one level up

    df = preprocess("data.csv")
    df.to_csv(ROOT / "processed_data.csv", index=False)

    real = keep_only_real_trials(df)

    compute_global_stats(real).to_csv(ROOT / "global_stats.csv", index=False)
    compute_duration_stats(real).to_csv(ROOT / "duration_stats.csv", index=False)
    participant_stats = compute_participant_stats(real)
    participant_stats.to_csv(ROOT / "participant_stats.csv", index=False)
    compute_difficulty_stats(real).to_csv(ROOT / "difficulty_stats.csv", index=False)
    rule_stats = compute_rule_stats(real)
    rule_stats.to_csv(ROOT / "rule_stats.csv", index=False)
    task_stats = compute_task_stats(real)
    task_stats.to_csv(ROOT / "task_stats.csv", index=False)

    plot_task_accuracy_hierarchical(task_stats)
    plot_task_accuracy_hierarchical_plain(task_stats)

    plot_rule_stats(rule_stats)
    plot_participant_accuracy(participant_stats)
    plot_participant_scatter(participant_stats)

    print("Done.")


if __name__ == "__main__":
    main()